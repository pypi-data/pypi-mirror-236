from johnsnowlabs import try_import_lib

if try_import_lib("haystack"):
    from johnsnowlabs.frameworks.embedding_retrival.haystack_node import (
        JSLHaystackEmbeddings,
    )

if try_import_lib("langchain"):
    from johnsnowlabs.frameworks.embedding_retrival.langchain_node import (
        JSLLangChainEmbeddings,
    )


if not try_import_lib("langchain") and not try_import_lib("haystack"):
    print(
        "Install either langchain or haystack and restart your python kernel to use the llm module!"
    )
