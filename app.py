from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os
from google.cloud import translate_v2 as translate

# .envファイルから環境変数を読み込む
load_dotenv()

# 以降のコードで、os.environ を使って環境変数にアクセスできる
credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")


app = Flask(__name__)

# サービスキーのパスが無効であるか確認
if not credentials_path:
    print("Error: GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
    exit(1)  # または適切なエラーハンドリングを行う

# サービスキーを用いてクライアントを初期化
try:
    translate_client = translate.Client.from_service_account_json(credentials_path)
except Exception as e:
    print(f"Error initializing translation client: {e}")
    exit(1)  # または適切なエラーハンドリングを行う

# ... (日英辞書の定義は変更なし) ...


def translate_to_japanese(text, target="ja"):
    """Google Translate APIを使ってテキストを日本語に翻訳する"""
    if not text:
        return ""

    try:
        result = translate_client.translate(text, target_language=target)
        return result["translatedText"]
    except Exception as e:
        print(f"Error during translation: {e}")
        return text


# 簡易的な日英辞書 (必要に応じて拡充)
ingredient_dictionary = {
    "鶏肉": "chicken",
    "鶏胸肉": "chicken breast",
    "豚肉": "pork",
    "牛肉": "beef",
    "玉ねぎ": "onion",
    "じゃがいも": "potato",
    "にんじん": "carrot",
    "トマト": "tomato",
    # ... 他の食材も追加 ...
}


def translate_to_english(ingredient_jp):
    """日本語の食材名を英語に翻訳する"""
    return ingredient_dictionary.get(ingredient_jp, ingredient_jp)


def search_recipes_by_ingredients(ingredients):
    """複数の食材からレシピを検索する"""
    base_url = "https://www.themealdb.com/api/json/v1/1/"
    endpoint = "filter.php"

    all_recipes = []
    for ingredient in ingredients:
        url = f"{base_url}{endpoint}?i={ingredient}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data and data["meals"]:
            all_recipes.extend(data["meals"])

    # 重複レシピを除外
    unique_recipes = {recipe["idMeal"]: recipe for recipe in all_recipes}.values()

    return list(unique_recipes)


def get_recipe_by_id(recipe_id):
    """レシピIDからレシピの詳細情報を取得し、一部を日本語に翻訳する"""
    base_url = "https://www.themealdb.com/api/json/v1/1/"
    endpoint = "lookup.php"
    url = f"{base_url}{endpoint}?i={recipe_id}"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    if data and data["meals"]:
        meal = data["meals"][0]
        # レシピ名と手順を日本語に翻訳
        meal["strMeal_ja"] = translate_to_japanese(meal["strMeal"])
        meal["strInstructions_ja"] = translate_to_japanese(meal["strInstructions"])

        # 材料名と計量単位を日本語に翻訳（Google Translate APIを使用）
        for i in range(1, 21):
            ingredient_key = f"strIngredient{i}"
            measure_key = f"strMeasure{i}"
            if meal[ingredient_key]:
                meal[ingredient_key + "_ja"] = translate_to_japanese(meal[ingredient_key])
            if meal[measure_key]:
                meal[measure_key + "_ja"] = translate_to_japanese(meal[measure_key])

    return data


# ... (他の関数は変更なし) ...


@app.route("/", methods=["GET", "POST"])
def index():
    recipes = []
    if request.method == "POST":
        user_input = request.form["ingredients"]
        ingredients_jp = [s.strip() for s in user_input.split(",")]
        ingredients_en = [translate_to_english(ingredient) for ingredient in ingredients_jp]
        recipes_summary = search_recipes_by_ingredients(ingredients_en)

        if recipes_summary:
            for recipe in recipes_summary[:3]:
                recipe_detail = get_recipe_by_id(recipe["idMeal"])
                if recipe_detail and recipe_detail["meals"]:
                    recipes.append(recipe_detail["meals"][0])

    return render_template("index.html", recipes=recipes)


if __name__ == "__main__":
    app.run(debug=True)
