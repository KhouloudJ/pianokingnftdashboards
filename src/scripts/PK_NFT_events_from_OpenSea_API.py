import requests
import json
import pandas as pd
import time

# Get al lthe event from a NFT token id
def get_events_from_token_id(token_id : int) -> list:
    url = f"https://api.opensea.io/api/v1/events?asset_contract_address=0x725afA0C34bab44f5b1ef8f87c50438F934c1A85&token_id={token_id}&only_opensea=false&offset=0&limit=50"
    headers = {
        "Accept": "application/json",
        "X-API-KEY": "14ce77f163994877be72b4ef5a281819"
    }
    response = requests.request("GET", url, headers=headers)
    json_data = json.loads(response.text)
    # We keep a waiting time to avoid a crash or reject from OpenSea
    time.sleep(0.4)
    return json_data["asset_events"]

# Get all the stats from a collection slug
def get_stats_from_collection_slug(collection_slug : str = "piano-king-nft") -> list:
    url = f"https://api.opensea.io/api/v1/collection/{collection_slug}/stats"
    headers = {"Accept": "application/json"}    
    response = requests.request("GET", url, headers=headers)
    json_data = json.loads(response.text)
    return json_data["stats"]
    
def result_if_dict_exists(_dict : dict, elem : str) -> str:
    return _dict.get(elem) if _dict else ""

def get_all_PK_NFT_event(total_number_of_PK_NFT : int):
    # Initialize the DataFrame to store Events
    final_df = pd.DataFrame(columns={
        "asset_id", 
        "asset_token_id",
        "asset_num_sales",
        "asset_image_url",
        "asset_name",
        "asset_contract_address",
        "asset_contract_created_date",
        "asset_contract_owner",
        "asset_contract_total_supply",
        "asset_permalink",
        "asset_owner_address",
        "asset_owner_username",
        "asset_bundle",
        "auction_type",
        "bid_amount",
        "collection_slug",
        "contract_address",
        "created_date",
        "custom_event_name",
        "dev_fee_payment_event",
        "dev_seller_fee_basis_points",
        "duration",
        "ending_price",
        "event_type",
        "from_account_address",
        "from_account_username",
        "id",
        "is_private",
        "owner_account",
        "payment_token_id",
        "payment_token_symbol",
        "payment_token_address",
        "payment_token_decimals",
        "payment_token_eth_price",
        "payment_token_usd_price",
        "quantity",
        "seller",
        "starting_price",
        "to_account",
        "total_price",
        "transaction",
        "winner_account",
        "listing_time"
        }
    )
    
    # For each PK NFT, we loop over all events
    for tk_id in range(1, total_number_of_PK_NFT):
        events_from_token_id = get_events_from_token_id(tk_id)
        # Loop over all events
        for event in events_from_token_id:
            asset_event = event.get("asset")
            from_account = event.get("from_account")
            to_account = event.get("to_account")
            seller = event.get("seller")
            payment_token = event.get("payment_token")
            transaction = event.get("transaction")
            winner_account = event.get("winner_account")
            final_df = final_df.append({
                "asset_id" : asset_event.get("id"), 
                "asset_token_id": asset_event.get("token_id"), 
                "asset_num_sales": asset_event.get("num_sales"), 
                "asset_image_url": asset_event.get("image_url"), 
                "asset_name": asset_event.get("name"), 
                "asset_contract_address": asset_event.get("contract_address"), 
                "asset_contract_created_date": asset_event.get("contract_created_date"), 
                "asset_contract_owner": asset_event.get("contract_owner"), 
                "asset_contract_total_supply": asset_event.get("contract_total_supply"), 
                "asset_permalink": asset_event.get("permalink"), 
                "asset_owner_address": asset_event.get("owner_address"), 
                "asset_owner_username": asset_event.get("owner_username"), 
                "asset_bundle": event.get("asset_bundle"), 
                "auction_type": event.get("auction_type"), 
                "bid_amount": event.get("bid_amount"), 
                "collection_slug": event.get("collection_slug"), 
                "contract_address": event.get("contract_address"), 
                "created_date": event.get("created_date"), 
                "custom_event_name": event.get("custom_event_name"), 
                "dev_fee_payment_event": event.get("dev_fee_payment_event"), 
                "dev_seller_fee_basis_points": event.get("dev_seller_fee_basis_points"), 
                "duration": event.get("duration"), 
                "ending_price": event.get("ending_price"), 
                "event_type": event.get("event_type"), 
                "from_account_address": result_if_dict_exists(from_account, "address"),
                "from_account_username": result_if_dict_exists(from_account, "username"), 
                "id": event.get("id"), 
                "is_private": event.get("is_private"), 
                "owner_account": event.get("owner_account"), 
                "payment_token_id": result_if_dict_exists(payment_token, "id"),
                "payment_token_symbol": result_if_dict_exists(payment_token, "symbol"),
                "payment_token_address": result_if_dict_exists(payment_token, "symbol"), 
                "payment_token_decimals": result_if_dict_exists(payment_token, "decimals"),
                "payment_token_eth_price": result_if_dict_exists(payment_token, "eth_price"),
                "payment_token_usd_price": result_if_dict_exists(payment_token, "usd_price"),
                "quantity": event.get("quantity"), 
                "seller_address": result_if_dict_exists(seller, "address"), 
                "seller_username": result_if_dict_exists(seller, "username"), 
                "starting_price": event.get("starting_price"), 
                "to_account_address": result_if_dict_exists(to_account, "address"), 
                "to_account_username": result_if_dict_exists(to_account, "username"),
                "total_price": event.get("total_price"), 
                "transaction_block_hash": result_if_dict_exists(transaction, "block_hash"), 
                "transaction_block_number": result_if_dict_exists(transaction, "block_number"),
                "transaction_id": result_if_dict_exists(transaction, "id"),
                "transaction_timestamp": result_if_dict_exists(transaction, "timestamp"),
                "transaction_hash": result_if_dict_exists(transaction, "transaction_hash"),
                "transaction_index": result_if_dict_exists(transaction, "transaction_index"),
                "winner_account_address": result_if_dict_exists(winner_account, "address"),
                "winner_account_username": result_if_dict_exists(winner_account, "username"),  
                "listing_time": event.get("listing_time")
                },
                ignore_index=True
            )
    
    #final_df.to_excel("resources/output/NFT_PK_events_from_OpenSea.xlsx")
    final_df.to_csv("resources/output/NFT_PK_events_from_OpenSea.csv")

if __name__ == '__main__':
    total_number_of_events = int(get_stats_from_collection_slug()['count'])
    get_all_PK_NFT_event(total_number_of_events)
    