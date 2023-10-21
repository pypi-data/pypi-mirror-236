import logging
import uuid

from tecton_core.offline_store import DeltaReader
from tecton_core.offline_store import OfflineStoreReaderParams
from tecton_core.query import nodes
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.node_utils import get_unified_tecton_data_source_dialect
from tecton_core.query.pandas import nodes as pandas_nodes
from tecton_core.query.query_tree_compute import QueryTreeCompute
from tecton_core.query.query_tree_compute import SnowflakeCompute
from tecton_core.query.sql_compat import Dialect


logger = logging.getLogger(__name__)


class PandasTreeRewriter:
    def rewrite(
        self,
        tree: NodeRef,
        pipeline_compute: QueryTreeCompute,
        data_source_compute: QueryTreeCompute,
    ) -> None:
        """Finds all FeatureViewPipelineNodes, executes their subtrees, and replaces them with StagedTableScanNodes."""
        tree_node = tree.node

        if isinstance(tree_node, nodes.FeatureViewPipelineNode):
            for _, fv_input_node_ref in tree_node.inputs_map.items():
                self._rewrite_fv_input_node(fv_input_node_ref, data_source_compute)

            pipeline_node = pandas_nodes.PandasFeatureViewPipelineNode.from_node_inputs(
                query_node=tree_node,
                input_node=None,
            )
            pipeline_result_df = pipeline_node.to_dataframe()
            staging_table_name = f"{pipeline_node.feature_definition_wrapper.name}_{uuid.uuid4().hex[:16]}_pandas"
            tree.node = nodes.StagedTableScanNode(
                tree_node.dialect,
                staged_columns=pipeline_node.columns,
                staging_table_name=staging_table_name,
            )
            pipeline_compute.register_temp_table_from_pandas(staging_table_name, pipeline_result_df)
        else:
            for i in tree.inputs:
                self.rewrite(tree=i, pipeline_compute=pipeline_compute, data_source_compute=data_source_compute)

    def _rewrite_fv_input_node(self, tree: NodeRef, data_source_compute: QueryTreeCompute) -> None:
        """Replaces a DataSourceScanNode that contains a Snowflake data source with a PandasDataNode."""
        if not isinstance(tree.node, nodes.DataSourceScanNode):
            return

        ds_dialect = get_unified_tecton_data_source_dialect(tree)
        if ds_dialect == Dialect.SNOWFLAKE:
            assert isinstance(
                data_source_compute, SnowflakeCompute
            ), "Data source compute must be SnowflakeCompute in order to rewrite Snowflake data source."
            sql_string = tree.node._to_query().get_sql()
            table = data_source_compute.run_sql(sql_string=sql_string, return_dataframe=True)

            # A rewrite should only leave NodeRefs. However, this PandasDataNode is only temporary. It will be removed
            # in 'rewrite' above.
            tree.node = pandas_nodes.PandasDataNode(
                input_df=table.to_pandas(),
                input_node=None,
                columns=tree.node.columns,
                column_name_updater=lambda x: x,
            )


class OfflineScanTreeRewriter:
    def rewrite(
        self,
        tree: NodeRef,
        pipeline_compute: QueryTreeCompute,
    ) -> None:
        for i in tree.inputs:
            self.rewrite(tree=i, pipeline_compute=pipeline_compute)

        tree_node = tree.node
        if isinstance(tree_node, nodes.OfflineStoreScanNode):
            fdw = tree_node.feature_definition_wrapper
            reader_params = OfflineStoreReaderParams(path=fdw.materialized_data_path)
            reader = DeltaReader(params=reader_params, fd=fdw)
            table = reader.read(tree_node.partition_time_filter)

            staged_table_name = f"{fdw.name}_offline_store_scan_{uuid.uuid4().hex[:16]}"
            pipeline_compute.register_temp_table(staged_table_name, table)
            tree.node = nodes.StagedTableScanNode(
                tree_node.dialect,
                staged_columns=tree_node.columns,
                staging_table_name=staged_table_name,
            )
