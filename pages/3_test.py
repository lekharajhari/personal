import streamlit as st
import requests
import concurrent.futures

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

        total_keys = len(secret_keys)
        st.write(f"Total Keys: {total_keys}")

        # Progress bar and progress text
        progress_bar = st.progress(0)
        progress_text = st.empty()

        available_balance_placeholder = st.empty()
        integration_off_placeholder = st.empty()
        invalid_key_count_placeholder = st.empty()

        available_balance_data = []
        integration_off_data = []
        invalid_key_count = 0

        def process_key(secret_key):
            result = get_sk_info(secret_key)
            if result:
                if 'error' in result:
                    if result['error'] == 'Failed to fetch account data':
                        return ('invalid', None)
                    elif result['error'] == 'Your account cannot currently make live charges.':
                        return ('integration_off', 
                            f"Secret Key: {secret_key} - Status: Integration off - "
                            f"Country: {result.get('country', 'Not available')} - "
                            f"Default Currency: {result.get('default_currency', 'Not available')}"
                        )
                    else:
                        return ('invalid', None)
                else:
                    if 'available_balance' in result:
                        return ('available_balance', 
                            f"Secret Key: {secret_key} - Status: Key is live - "
                            f"Available Balance: {result['available_balance']} - "
                            f"Country: {result.get('country', 'Not available')} - "
                            f"Currency: {result.get('currency', 'Not available')} - "
                            f"Pending Balance: {result.get('pending_balance', 'Not available')}"
                        )
                    else:
                        return ('invalid', None)
            else:
                return ('invalid', None)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = []
            for idx, result in enumerate(executor.map(process_key, secret_keys), 1):
                results.append(result)

                # Update progress
                progress_percentage = idx / total_keys
                progress_bar.progress(progress_percentage)
                progress_text.write(f"Processing key {idx} of {total_keys}")

        for status, message in results:
            if status == 'available_balance':
                available_balance_data.append(message)
            elif status == 'integration_off':
                integration_off_data.append(message)
            elif status == 'invalid':
                invalid_key_count += 1

        with available_balance_placeholder.container():
            for data in available_balance_data:
                st.success(data)

        with integration_off_placeholder.container():
            for data in integration_off_data:
                st.warning(data)

        with invalid_key_count_placeholder.container():
            st.write(f"Invalid Keys: {invalid_key_count}")

if __name__ == "__main__":
    main()