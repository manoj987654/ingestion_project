def build_params(pagination, page):

    if not pagination:
        return {}

    page_size = pagination.get("page_size", 10)

    strategy = pagination.get("page_strategy", "page")

    if strategy == "offset":

        return {
            pagination["page_param"]: page * page_size,
            pagination["page_size_param"]: page_size
        }

    return {
        pagination["page_param"]: page + 1,
        pagination["page_size_param"]: page_size
    }