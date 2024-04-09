import requests

def get_bot_id(token: str):
    headers = {
        'Authorization': f'Bot {token}'
    }
    try:
        response = requests.get('https://discord.com/api/v10/users/@me', headers=headers)
        response.raise_for_status()
        data = response.json()
        return data['id']
    except Exception as e:
        print(f"Error fetching bot ID for token {token}: {e}")
        return None

def token_to_oauth2(token: str):
    print(f"Converting token {token} to OAuth2 link...")
    bot_id = get_bot_id(token)
    print(f"Bot ID for token {token}: {bot_id}")
    if bot_id:
        base_url = "https://discord.com/oauth2/authorize"
        return f"{base_url}?client_id={bot_id}&permissions=0&scope=bot"
    else:
        return None

def convert_tokens_to_oauth2(input_file: str, output_file: str):
    try:
        with open(input_file, 'r') as file:
            tokens = [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"File '{input_file}' not found.")
        return

    oauth2_links = [token_to_oauth2(token) for token in tokens]

    try:
        with open(output_file, 'w') as out_file:
            for link in oauth2_links:
                if link:
                    out_file.write(link + '\n')
        print(f"OAuth2 links written to {output_file}")
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")

if __name__ == "__main__":
    input_file = "tokens.txt"
    output_file = "oauth2.txt"
    convert_tokens_to_oauth2(input_file, output_file)
