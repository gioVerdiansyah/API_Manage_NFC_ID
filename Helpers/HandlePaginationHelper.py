import re


def get_paginated_data(cursor, page=1, per_page=5):
    """
    Function to get paginated data and convert ObjectId to string.

    :param cursor: MongoDB cursor object
    :param page: Current page number (1-indexed, default 1)
    :param per_page: Number of items per page (default 10)
    :return: Dictionary containing paginated data and metadata
    """
    if not isinstance(page, int) or page < 1:
        raise ValueError("Page number must be a positive integer.")
    if not isinstance(per_page, int) or per_page < 1:
        raise ValueError("Items per page must be a positive integer.")

    skips = per_page * (page - 1)
    paginated_cursor = cursor.skip(skips).limit(per_page)

    # Convert ObjectId to string
    documents = []
    for doc in paginated_cursor:
        doc['_id'] = str(doc['_id'])
        doc['was_purchased'] = len(doc['was_purchased'])
        documents.append(doc)

    # Get total count of documents in cursor (for pagination metadata)
    total_count = cursor.collection.count_documents(cursor._Cursor__spec)

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
            "last_page": total_pages,
            "next_page": next_page,
            "prev_page": prev_page
        }
    }

    return response


def get_paginated_data_user_purchased(query, page=1, per_page=5, search_id=None):
    skip = (page - 1) * per_page
    responses = []

    for doc in query:
        machine_name = doc.get('machine_name')
        scene_id = doc.get('scene_id')

        for purchase in doc['was_purchased']:
            if search_id:
                print(purchase['id'])
                id_match = re.search(search_id, purchase['id'], re.IGNORECASE)
                if not id_match:
                    continue

            purchase_data = {
                "machine_name": machine_name,
                "scene_id": scene_id,
                "id": purchase['id'],
                "buy_at": purchase['buy_at'],
                "isUsed": purchase['isUsed'],
                "last_used": purchase['last_used'],
                "total_used": purchase['total_used']
            }
            responses.append(purchase_data)

    total_count = len(responses[skip: skip + per_page])
    total_pages = (len(responses) + per_page - 1) // per_page
    has_next_page = page < total_pages
    next_page = page + 1 if has_next_page else None
    has_prev_page = page > 1
    prev_page = page - 1 if has_prev_page else None

    pagination = {
        "total_per_data": total_count,
        "current_page": page,
        "per_page": per_page,
        "last_page": total_pages,
        "next_page": next_page,
        "prev_page": prev_page
    }

    return {"data": responses[skip: skip + per_page], "pagination": pagination}


def get_paginate_data_with_search(query, page=1, per_page=5, search_keyword=None):
    skip = (page - 1) * per_page
    responses = []

    for doc in query:
        machine_name = doc.get('machine_name')
        scene_id = doc.get('scene_id')
        matched_purchases = []

        for purchase in doc['was_purchased']:
            if not search_keyword or re.search(search_keyword, purchase['id'], re.IGNORECASE):
                purchase_data = {
                    "machine_name": machine_name,
                    "scene_id": scene_id,
                    "id": purchase['id'],
                    "buy_at": purchase['buy_at'],
                    "isUsed": purchase['isUsed'],
                    "last_used": purchase['last_used'],
                    "total_used": purchase['total_used']
                }
                matched_purchases.append(purchase_data)

        responses.extend(matched_purchases)

    total_count = len(responses)
    total_pages = (total_count + per_page - 1) // per_page
    paginated_responses = responses[skip: skip + per_page]

    has_next_page = page < total_pages
    next_page = page + 1 if has_next_page else None
    has_prev_page = page > 1
    prev_page = page - 1 if has_prev_page else None

    pagination = {
        "total_per_data": len(paginated_responses),
        "current_page": page,
        "per_page": per_page,
        "last_page": total_pages,
        "next_page": next_page,
        "prev_page": prev_page
    }

    return {"data": paginated_responses, "pagination": pagination}
