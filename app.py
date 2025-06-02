from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/region-info/<region>/<uid>', methods=['GET'])
def get_player_info(region, uid):
    try:
        url = f"https://nr-codex-info1.vercel.app/player-info?region={region}&uid={uid}"
        response = requests.get(url)
        
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch data from the original API"}), response.status_code

        data = response.json()

        filtered_data = {
            "AccountRegion": data.get("AccountInfo", {}).get("AccountRegion"),
            "ReleaseVersion": data.get("AccountInfo", {}).get("ReleaseVersion"),
            "AccountName": data.get("AccountInfo", {}).get("AccountName"),
            "AccountLastLogin": data.get("AccountInfo", {}).get("AccountLastLogin"),
            "AccountLevel": data.get("AccountInfo", {}).get("AccountLevel"),
            "AccountLikes": data.get("AccountInfo", {}).get("AccountLikes"),
            "GuildName": data.get("GuildInfo", {}).get("GuildName")
        }

        return jsonify(filtered_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
