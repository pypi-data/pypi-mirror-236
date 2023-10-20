from .checkpointing import StreamingCheckpointer
from .easylm import with_sharding_constraint, match_partition_rules, wrap_function_with_rng, tree_apply, \
    names_in_current_mesh, flatten_tree, get_jax_mesh, cross_entropy_loss_and_accuracy, tree_path_to_string, \
    average_metrics, float_tensor_to_dtype, get_float_dtype_by_name, float_to_dtype, get_metrics, \
    get_gradient_checkpoint_policy, get_names_from_partition_spec, global_norm, get_weight_decay_mask, mse_loss, \
    named_tree_map, make_shard_and_gather_fns, blockwise_cross_entropy, blockwise_dot_product_attention
from .load import load_pretrained_model
from .utils import change_to_fp16, change_to_fp32, change_to_bf16, change, count_params, get_names, get_devices, \
    transpose
from .flash_attention import dot_product_attention_queries_per_head, dot_product_attention_multihead, \
    dot_product_attention_multiquery, _memory_efficient_attention

__version__ = '0.0.17'
