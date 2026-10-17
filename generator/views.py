
import json
import os

from django.shortcuts import render
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# True  = Use predefined sample tweets without API calls.
# False = Generate tweets using Gemini AI.
DEMO_MODE = True


def home(request):
    """Display the brand details form."""
    return render(request, "generator/home.html")


def generate_tweets(request):
    """Analyze brand details and generate 10 tweet suggestions."""

    if request.method != "POST":
        return render(request, "generator/home.html")

    # --------------------------------------------------
    # 1. Read form data
    # --------------------------------------------------

    brand_name = request.POST.get("brand_name", "").strip()
    industry = request.POST.get("industry", "").strip()
    objective = request.POST.get("objective", "").strip()
    products = request.POST.get("products", "").strip()
    audience = request.POST.get("audience", "").strip()
    tone = request.POST.get("tone", "").strip()
    brand_description = request.POST.get(
        "brand_description", ""
    ).strip()

    context = {
        "brand_name": brand_name,
        "industry": industry,
        "objective": objective,
        "products": products,
        "audience": audience,
        "tone": tone,
        "brand_description": brand_description,
        "voice_label": "Inferred Brand Voice",
    }

    # --------------------------------------------------
    # 2. Validate required fields
    # --------------------------------------------------

    if not brand_name or not industry or not audience or not tone:
        context["error"] = (
            "Please fill in the brand name, industry, "
            "target audience, and preferred tone."
        )

        return render(
            request,
            "generator/results.html",
            context,
        )

    # --------------------------------------------------
    # 3. Analyze the submitted brand details
    # --------------------------------------------------

    voice_summary = [
        (
            f"The communication style is {tone.lower()} "
            "and audience-focused."
        ),
        (
            f"The messaging supports the objective: "
            f"{objective or 'Brand Awareness'}."
        ),
        f"The content is designed for {audience}.",
        (
            f"The brand focuses on {products}."
            if products
            else "The content focuses on the brand's core offering."
        ),
    ]

    # --------------------------------------------------
    # 4. DEMO MODE: Brand-specific sample tweets
    # --------------------------------------------------

    if DEMO_MODE:

        brand = brand_name.lower()

        # ================ STARBUCKS ================

        if "starbucks" in brand:

            demo_tweets = [
                {
                    "text": (
                        "A little coffee, a little comfort, "
                        "and a moment just for you. ☕"
                    ),
                    "purpose": "Connect coffee with everyday moments.",
                },
                {
                    "text": (
                        "Good conversations often begin "
                        "with a cup of coffee."
                    ),
                    "purpose": "Encourage connection and conversation.",
                },
                {
                    "text": (
                        "Your coffee break called. It's time "
                        "to slow down and enjoy the moment."
                    ),
                    "purpose": "Promote a relaxing coffee break.",
                },
                {
                    "text": (
                        "From your first sip to your last task, "
                        "make today your own."
                    ),
                    "purpose": "Connect coffee with daily routines.",
                },
                {
                    "text": (
                        "Coffee tastes even better when shared "
                        "with someone special."
                    ),
                    "purpose": "Encourage social connection.",
                },
                {
                    "text": (
                        "Big plans or quiet moments? "
                        "There's room for both over coffee."
                    ),
                    "purpose": (
                        "Position coffee as part of everyday experiences."
                    ),
                },
                {
                    "text": (
                        "Take a breath, enjoy your favorite cup, "
                        "and make space for yourself."
                    ),
                    "purpose": "Promote a moment of personal comfort.",
                },
                {
                    "text": (
                        "Catch up with a friend, share a laugh, "
                        "and let the coffee flow."
                    ),
                    "purpose": "Encourage customers to connect over coffee.",
                },
                {
                    "text": (
                        "Some of life's favorite moments happen "
                        "one sip at a time."
                    ),
                    "purpose": "Build an emotional connection with the brand.",
                },
                {
                    "text": (
                        "Make your next coffee moment "
                        "one worth remembering."
                    ),
                    "purpose": "Encourage a memorable café experience.",
                },
            ]

        # ================= NIKE ====================

        elif "nike" in brand:

            demo_tweets = [
                {
                    "text": (
                        "Every step forward brings you closer "
                        "to your goals. Keep moving. #JustDoIt"
                    ),
                    "purpose": "Inspire people to keep progressing.",
                },
                {
                    "text": (
                        "Your limits are challenges waiting "
                        "to be overcome."
                    ),
                    "purpose": "Encourage people to challenge their limits.",
                },
                {
                    "text": (
                        "Greatness begins when you decide to start. "
                        "Take that first step."
                    ),
                    "purpose": "Motivate people to take action.",
                },
                {
                    "text": (
                        "Train with purpose. Move with confidence. "
                        "Believe in yourself."
                    ),
                    "purpose": "Promote confidence and purposeful training.",
                },
                {
                    "text": (
                        "The strongest competition is the person "
                        "you were yesterday."
                    ),
                    "purpose": "Encourage personal improvement.",
                },
                {
                    "text": (
                        "Big goals begin with small steps. "
                        "Make every effort count."
                    ),
                    "purpose": "Connect daily effort with long-term goals.",
                },
                {
                    "text": (
                        "When the challenge gets tough, "
                        "remember why you started."
                    ),
                    "purpose": "Encourage persistence.",
                },
                {
                    "text": (
                        "Your journey. Your effort. "
                        "Your next breakthrough."
                    ),
                    "purpose": "Celebrate individual athletic progress.",
                },
                {
                    "text": (
                        "Don't wait for motivation. "
                        "Take action and build momentum."
                    ),
                    "purpose": "Encourage an active mindset.",
                },
                {
                    "text": (
                        "Show up, put in the work, "
                        "and give your goals a chance."
                    ),
                    "purpose": "Promote consistency and commitment.",
                },
            ]

        # =============== OTHER BRANDS ===============

        else:

            demo_tweets = [
                {
                    "text": (
                        f"Discover what makes {brand_name} "
                        "part of your everyday story."
                    ),
                    "purpose": "Build brand awareness.",
                },
                {
                    "text": (
                        f"Every day is an opportunity to experience "
                        f"{brand_name} in a new way."
                    ),
                    "purpose": "Encourage customers to explore the brand.",
                },
                {
                    "text": (
                        f"Your needs, your goals, your journey. "
                        f"{brand_name} is here to be part of it."
                    ),
                    "purpose": "Connect the brand with its audience.",
                },
                {
                    "text": (
                        f"Make room for more of what matters "
                        f"with {brand_name}."
                    ),
                    "purpose": "Create an emotional connection.",
                },
                {
                    "text": (
                        f"Looking for something that fits your lifestyle? "
                        f"Discover {brand_name}."
                    ),
                    "purpose": "Encourage brand discovery.",
                },
                {
                    "text": (
                        f"Small moments can make a big difference. "
                        f"Make yours count with {brand_name}."
                    ),
                    "purpose": "Associate the brand with meaningful moments.",
                },
                {
                    "text": (
                        f"Get inspired, explore possibilities, "
                        f"and discover {brand_name}."
                    ),
                    "purpose": "Encourage engagement with the brand.",
                },
                {
                    "text": (
                        f"Your next favorite experience could start "
                        f"with {brand_name}."
                    ),
                    "purpose": "Spark curiosity about the brand.",
                },
                {
                    "text": (
                        f"Different goals, different journeys, "
                        f"one place to discover: {brand_name}."
                    ),
                    "purpose": "Highlight the brand's relevance.",
                },
                {
                    "text": (
                        f"What's your next step? Let {brand_name} "
                        "be part of the journey."
                    ),
                    "purpose": "Encourage the audience to take action.",
                },
            ]

        context["voice_summary"] = voice_summary
        context["tweets"] = demo_tweets
        context["generation_mode"] = (
            "Demo Mode — Brand-specific sample tweets "
            "(not generated by AI)"
        )

        return render(
            request,
            "generator/results.html",
            context,
        )

    # --------------------------------------------------
    # 5. LIVE GEMINI AI MODE
    # --------------------------------------------------

    if not GEMINI_API_KEY:
        context["error"] = (
            "Gemini API key not found. "
            "Please check your .env file."
        )

        return render(
            request,
            "generator/results.html",
            context,
        )

    prompt = f"""
You are BrandVoice AI, an expert social media copywriter.

Create exactly 10 original tweets and a brand voice summary.

Brand name: {brand_name}
Industry: {industry}
Objective: {objective}
Products: {products}
Target audience: {audience}
Preferred tone: {tone}
Brand description: {brand_description}

Requirements:
1. Generate exactly 10 distinct tweets.
2. Adapt every tweet to this specific brand.
3. Keep tweets concise and suitable for X.
4. Match the brand tone, audience, and objective.
5. Do not invent statistics, offers, or product claims.
6. Infer brand voice from the submitted information.
7. Return valid JSON only, without Markdown fences.

Use this JSON structure:
{{
    "voice_summary": [
        "Observation 1",
        "Observation 2",
        "Observation 3",
        "Observation 4"
    ],
    "tweets": [
        {{
            "text": "Tweet text",
            "purpose": "Tweet purpose"
        }}
    ]
}}
"""

    try:
        client = genai.Client(
            api_key=GEMINI_API_KEY,
            http_options={"timeout": 15000},
        )

        response = client.interactions.create(
            model="gemini-3.8-flash",
            input=prompt,
        )

        response_text = (response.output_text or "").strip()

        # Remove Markdown fences if present.
        if response_text.startswith("```"):
            response_text = response_text.split("\n", 1)[1]

            if response_text.endswith("```"):
                response_text = response_text[:-3].strip()

        data = json.loads(response_text)

        voice_summary = data.get("voice_summary", [])
        tweets = data.get("tweets", [])

        if not isinstance(voice_summary, list):
            raise ValueError("Invalid brand voice summary.")

        if not isinstance(tweets, list) or len(tweets) != 10:
            raise ValueError(
                "The AI did not return exactly 10 tweets."
            )

        for tweet in tweets:
            if (
                not isinstance(tweet, dict)
                or not tweet.get("text")
                or not tweet.get("purpose")
            ):
                raise ValueError("A generated tweet is invalid.")

        context["voice_summary"] = voice_summary
        context["tweets"] = tweets
        context["generation_mode"] = "Gemini AI Generated"

    except Exception as error:
        print(
            "BrandVoice AI generation error:",
            repr(error),
        )

        error_text = str(error).lower()

        if (
            "429" in error_text
            or "resource_exhausted" in error_text
            or "too many requests" in error_text
        ):
            context["error"] = (
                "The Gemini API quota has been reached. "
                "Please wait for the quota to reset before "
                "trying live AI generation again."
            )

        elif "timeout" in error_text or "timed out" in error_text:
            context["error"] = (
                "The AI request timed out. "
                "Please try again later."
            )

        else:
            context["error"] = (
                "Tweet generation failed. "
                "Check the VS Code terminal for details."
            )

    return render(
        request,
        "generator/results.html",
        context,
    )

