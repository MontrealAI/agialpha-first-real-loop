

def validate_installation_record(data: dict) -> tuple[bool, list[str]]:
    errs=[]
    if 'public_display_allowed' not in data: errs.append('public_display_allowed missing')
    if data.get('human_review_required') is not True: errs.append('human_review_required must be true')
    dh=data.get('data_handling',{})
    if dh.get('raw_secret_ingestion_allowed') is True: errs.append('raw_secret_ingestion_allowed forbidden')
    if dh.get('personal_data_intended') is True: errs.append('personal_data_intended forbidden')
    if dh.get('store_full_webhook_payload') is True: errs.append('store_full_webhook_payload forbidden by default')
    return (len(errs)==0, errs)
