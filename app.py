import os
import json
import datetime
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure Google Gemini API
# Load variables from .env file if it exists (for local development)
env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_path):
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip()
    except Exception as e:
        print(f"Error loading .env file: {e}")

api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

FEEDBACK_FILE = os.path.join(os.path.dirname(__file__), "feedback_data.json")

def load_feedback():
    if not os.path.exists(FEEDBACK_FILE):
        return []
    try:
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_feedback(data):
    try:
        with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving feedback: {e}")

# 12 Prompt Engineering templates: 4 Functions x 3 Style Variants
PROMPT_TEMPLATES = {
    "qa": {
        "1": {
            "name": "Factual & Direct",
            "description": "Concise, plain facts (under 2 paragraphs).",
            "template": "You are a factual assistant. Provide a direct, concise, and accurate answer to the following question. Avoid introductory filler and wrap up in 1-2 paragraphs max.\n\nQuestion:\n{input_text}"
        },
        "2": {
            "name": "Comprehensive Explainer",
            "description": "Pedagogical, in-depth explanation with examples.",
            "template": "You are an educator. Provide a comprehensive, detailed explanation of the user's query. Include background context, key concepts, real-world examples, and explain the significance of the topic. Write in a clear, pedagogical tone.\n\nQuery:\n{input_text}"
        },
        "3": {
            "name": "Structured Outline",
            "description": "Bulleted breakdown highlighting key concepts.",
            "template": "You are an analytical assistant. Break down the answer to the user's question into clear, structured bullet points. Use bold terms for key concepts and start with a brief 1-sentence introduction.\n\nQuestion:\n{input_text}"
        }
    },
    "summary": {
        "1": {
            "name": "Short Summary",
            "description": "Quick 1-paragraph overview (under 80 words).",
            "template": "You are a summarization tool. Condense the provided text into a single concise paragraph (under 80 words) capturing the main point.\n\nText:\n{input_text}"
        },
        "2": {
            "name": "Key Takeaways",
            "description": "Action-oriented bulleted points of core ideas.",
            "template": "You are an expert analyst. Extract the key takeaways from the provided text as a structured list of bullet points (maximum 5 points). Ensure each bullet point is clear, action-oriented, and captures a core idea.\n\nText:\n{input_text}"
        },
        "3": {
            "name": "Executive Briefing",
            "description": "Professional report with themes and implications.",
            "template": "You are a business consultant. Analyze the provided text and write a professional Executive Brief. Include sections for: 1. Core Summary, 2. Key Themes, and 3. Practical Implications.\n\nText:\n{input_text}"
        }
    },
    "creative": {
        "1": {
            "name": "Poetic & Vivid",
            "description": "Artistic content focusing on rich imagery and metaphors.",
            "template": "You are a poet and creative writer. Write highly descriptive, emotional, and artistic content based on the user's request. Focus on rich imagery, sensory details, and evocative metaphors.\n\nRequest:\n{input_text}"
        },
        "2": {
            "name": "Narrative Story",
            "description": "Engaging story with setting, character, and plot.",
            "template": "You are a novelist. Write an engaging narrative story based on the user's prompt. Establish a clear setting, introduce a compelling character arc, and use dialogue if appropriate to build tension.\n\nPrompt:\n{input_text}"
        },
        "3": {
            "name": "Minimalist Expression",
            "description": "Short haiku (5-7-5 structure) or single-sentence story.",
            "template": "You are a minimalist writer. Express the user's prompt in the shortest form possible—either a haiku (5-7-5 syllable structure) or a 1-sentence micro-fiction story.\n\nPrompt:\n{input_text}"
        }
    },
    "advisor": {
        "1": {
            "name": "Empathetic Coach",
            "description": "Encouraging, supportive study advice.",
            "template": "You are a supportive academic coach. Provide encouraging, warm, and highly motivational advice on the user's learning query. Highlight the user's potential and offer general strategies to stay focused and positive.\n\nQuery:\n{input_text}"
        },
        "2": {
            "name": "Structured Roadmap",
            "description": "Week-by-week plan with milestones and techniques.",
            "template": "You are a curriculum architect. Break down the user's learning goal into a highly structured, week-by-week study roadmap. Include specific topics, suggested resources/techniques, and clear milestones for each stage.\n\nLearning Goal:\n{input_text}"
        },
        "3": {
            "name": "Critique & Troubleshoot",
            "description": "Identify potential pitfalls and offer practical tips.",
            "template": "You are a critical reviewer. Evaluate the user's learning goals or study methods. Identify potential pitfalls, typical mistakes students make in this area, and offer practical, cautious troubleshooting tips.\n\nGoal/Method:\n{input_text}"
        }
    }
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "Invalid JSON payload."}), 400

        func = data.get("function")
        style = data.get("style")
        input_text = data.get("input_text", "").strip()

        if not func or not style or not input_text:
            return jsonify({"success": False, "error": "Missing required fields."}), 400

        if func not in PROMPT_TEMPLATES or style not in PROMPT_TEMPLATES[func]:
            return jsonify({"success": False, "error": "Invalid function or style selection."}), 400

        template_info = PROMPT_TEMPLATES[func][style]
        raw_prompt = template_info["template"].format(input_text=input_text)

        response = model.generate_content(raw_prompt)
        response_text = response.text

        return jsonify({
            "success": True,
            "raw_prompt": raw_prompt,
            "response": response_text
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/feedback", methods=["POST"])
def feedback():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "Invalid JSON payload."}), 400

        func = data.get("function")
        style = data.get("style")
        input_text = data.get("input_text")
        raw_prompt = data.get("raw_prompt")
        response_text = data.get("response_text")
        rating = data.get("rating")  # "like" or "dislike"
        comment = data.get("comment", "")

        if not func or not style or not rating:
            return jsonify({"success": False, "error": "Missing rating parameters."}), 400

        feedbacks = load_feedback()
        feedbacks.append({
            "id": len(feedbacks) + 1,
            "timestamp": datetime.datetime.now().isoformat(),
            "function": func,
            "style": style,
            "style_name": PROMPT_TEMPLATES.get(func, {}).get(style, {}).get("name", "Unknown"),
            "input_text": input_text,
            "raw_prompt": raw_prompt,
            "response_text": response_text,
            "rating": rating,
            "comment": comment
        })
        save_feedback(feedbacks)

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/analytics", methods=["GET"])
def analytics():
    try:
        feedbacks = load_feedback()
        total_requests = len(feedbacks)
        likes = sum(1 for f in feedbacks if f.get("rating") == "like")
        dislikes = sum(1 for f in feedbacks if f.get("rating") == "dislike")
        helpfulness_rate = (likes / total_requests * 100) if total_requests > 0 else 0

        # Breakdowns per function
        function_stats = {}
        for func in ["qa", "summary", "creative", "advisor"]:
            func_feedbacks = [f for f in feedbacks if f.get("function") == func]
            func_total = len(func_feedbacks)
            func_likes = sum(1 for f in func_feedbacks if f.get("rating") == "like")
            func_rate = (func_likes / func_total * 100) if func_total > 0 else 0
            
            # Count details per variant
            style_stats = {}
            for style in ["1", "2", "3"]:
                style_feedbacks = [f for f in func_feedbacks if f.get("style") == style]
                style_total = len(style_feedbacks)
                style_likes = sum(1 for f in style_feedbacks if f.get("rating") == "like")
                style_rate = (style_likes / style_total * 100) if style_total > 0 else 0
                style_name = PROMPT_TEMPLATES[func][style]["name"]
                style_stats[style] = {
                    "name": style_name,
                    "total": style_total,
                    "rate": round(style_rate, 1)
                }

            function_stats[func] = {
                "total": func_total,
                "rate": round(func_rate, 1),
                "styles": style_stats
            }

        # Recent logs (last 10)
        recent_logs = []
        for f in reversed(feedbacks[-10:]):
            recent_logs.append({
                "timestamp": f.get("timestamp"),
                "function": f.get("function").upper(),
                "style_name": f.get("style_name"),
                "input_text": f.get("input_text", "")[:70] + ("..." if len(f.get("input_text", "")) > 70 else ""),
                "rating": f.get("rating"),
                "comment": f.get("comment", "")
            })

        return jsonify({
            "total_requests": total_requests,
            "likes": likes,
            "dislikes": dislikes,
            "helpfulness_rate": round(helpfulness_rate, 1),
            "function_stats": function_stats,
            "recent_logs": recent_logs
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)