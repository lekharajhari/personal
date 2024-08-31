import streamlit as st
import requests
import pandas as pd

def get_sk_info(secret_key: str) -> dict:
    url = f"https://api.voidex.dev/api/skinfo?sk={secret_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Request failed: {e}")
        return None

def main():
    st.title("Stripe Secret Key Info")
    file_upload = st.file_uploader("Upload a text file with Stripe secret keys (one key per line):", type=["txt"])

    if file_upload:
        file_content = file_upload.read().decode("utf-8")
        secret_keys = [line.strip() for line in file_content.splitlines()]

        available_balance_data = []
        integration_off_data = []
        invalid_key_data = []

        for secret_key in secret_keys:
            result = get_sk_info(secret_key)

            if result:
                if 'error' in result:
                    if result['error'] == 'Failed to fetch account data':
                        invalid_key_data.append({"Secret Key": secret_key, "Status": "Invalid key"})
                    elif result['error'] == 'Your account cannot currently make live charges.':
                        integration_off_data.append({
                            "Secret Key": secret_key,
                            "Status": "Integration off",
                            "Country": result.get('country', 'Not available'),
                            "Default Currency": result.get('default_currency', 'Not available')
                        })
                    else:
                        invalid_key_data.append({"Secret Key": secret_key, "Status": "Error", "Error": result['error']})
                else:
                    if 'available_balance' in result:
                        available_balance_data.append({
                            "Secret Key": secret_key,
                            "Status": "Key is live",
                            "Available Balance": result['available_balance'],
                            "Country": result.get('country', 'Not available'),
                            "Currency": result.get('currency', 'Not available'),
                            "Pending Balance": result.get('pending_balance', 'Not available')
                        })
                    else:
                        invalid_key_data.append({"Secret Key": secret_key, "Status": "Key is not present or available balance is not available."})
            else:
                invalid_key_data.append({"Secret Key": secret_key, "Status": "Failed to retrieve information about the secret key."})

        st.header("Available Balance")
        available_balance_df = pd.DataFrame(available_balance_data)
        st.success("Available Balance")
        st.table(available_balance_df)

        st.header("Integration Off")
        integration_off_df = pd.DataFrame(integration_off_data)
        st.warning("Integration Off")
        st.table(integration_off_df)

        st.header("Invalid Keys")
        invalid_key_df = pd.DataFrame(invalid_key_data)
        st.error("Invalid Keys")
        st.table(invalid_key_df)

if __name__ == "__main__":
    main()