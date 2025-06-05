from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/region-info/<uid>', methods=['GET'])
def get_player_info(uid):
    try:
        # Pehle 'ind' try karega, agar fail ho to 'bd'
        regions_to_try = ['ind', 'bd']
        final_data = None

        for region in regions_to_try:
            url = f"https://nr-codex-info1.vercel.app/player-info?region={region}&uid={uid}"
            response = requests.get(url)

            # Agar API call fail ho gayi to next region try kare
            if response.status_code != 200:
                continue

            data = response.json()

            # Agar valid AccountRegion mila to data extract kare
            if data.get("AccountInfo", {}).get("AccountRegion"):
                final_data = {
                    "AccountRegion": data.get("AccountInfo", {}).get("AccountRegion"),
                    "ReleaseVersion": data.get("AccountInfo", {}).get("ReleaseVersion"),
                    "AccountName": data.get("AccountInfo", {}).get("AccountName"),
                    "AccountLastLogin": data.get("AccountInfo", {}).get("AccountLastLogin"),
                    "AccountLevel": data.get("AccountInfo", {}).get("AccountLevel"),
                    "AccountLikes": data.get("AccountInfo", {}).get("AccountLikes"),
                    "GuildName": data.get("GuildInfo", {}).get("GuildName")
                }
                break  # Jisme valid data mil gaya usi pe ruk jao

        # Agar data mil gaya to return karo
        if final_data:
            return jsonify(final_data), 200
        else:
            return jsonify({"error": "No valid data found for given UID in any region."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
