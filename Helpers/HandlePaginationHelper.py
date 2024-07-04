import os
def get_paginated_data(collection, page, per_page=1):
    """
    Function to get paginated data and convert ObjectId to string.

    :param collection: MongoDB collection object
    :param page: Current page number (1-indexed)
    :param per_page: Number of items per page (default 10)
    :return: Dictionary containing paginated data and metadata
    """
    if not isinstance(page, int) or page < 1:
        raise ValueError("Page number must be a positive integer.")
    if not isinstance(per_page, int) or per_page < 1:
        raise ValueError("Items per page must be a positive integer.")

    skips = per_page * (page - 1)
    cursor = collection.find().skip(skips).limit(per_page)

    # Convert ObjectId to string
    documents = []
    for doc in cursor:
        doc['_id'] = str(doc['_id'])
        documents.append(doc)

    # Get total count of documents in collection (for pagination metadata)
    total_count = collection.count_documents({})

    # Calculate pagination metadata
    total_pages = (total_count + per_page - 1) // per_page
    has_next_page = page < total_pages
    next_page = page + 1 if has_next_page else None
    has_prev_page = page > 1
    prev_page = page - 1 if has_prev_page else None

    # Prepare response dictionary
    response = {
        "data": documents,
        "pagination": {
            "total_per_data": len(documents),
            "current_page": page,
            "per_page": per_page,
            "total": total_count,
            "last_page": total_pages,
            "next_page": next_page,
            "prev_page": prev_page
        }
    }

    return response
