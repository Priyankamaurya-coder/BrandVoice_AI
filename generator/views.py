
import json
import os
import re

from django.shortcuts import render
from google import genai


# Read the Gemini API key from environment variables.
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")


def home(request):
    """Display the BrandVoice AI input form."""
    return render(request, "generator/home.html")


def generate_tweets(request):
    """Generate brand-specific tweets using Gemini AI."""

    if request.method != "POST":
        return render(request, "generator/home.html")

    # Collect form inputs.
    brand_name = request.POST.get("brand_name", "").strip()
    industry = request.POST.get("industry", "").strip()
    objective = request.POST.get("objective", "").strip()
    products = request.POST.get("products", "").strip()
    audience = request.POST.get("audience", "").strip()
    tone = request.POST.get("tone", "AI Infer").strip()
    brand_description = request.POST.get(
        "brand_description", ""
    ).strip()

    # Validate required fields.
    if not brand_name or not industry or not audience or not tone:
        return render(
            request,
            "generator/home.html",
            {
                "error": (
                    "Please fill in the brand name, industry, "
                    "target audience, and tone."
                )
            },
        )

    # Provide defaults for optional fields.
    objective = objective or "Brand Awareness"
    products = products or "General brand offerings"
    brand_description = (
        brand_description
        or "Infer the brand's communication style from the supplied details."
    )

    # Display the submitted brand information on the results page.
    voice_summary = [
        f"Tone: {tone}",
        f"Target audience: {audience}",
        f"Campaign objective: {objective}",
        f"Industry and offerings: {industry}; {products}",
    ]

    # Shared context ensures the brand description is available
    # even if AI generation fails.
    base_context = {
        "brand_name": brand_name,
        "industry": industry,
        "objective": objective,
        "products": products,
        "audience": audience,
        "tone": tone,
        "brand_description": brand_description,
        "voice_summary": voice_summary,
        "tweets": [],
    }

    # Check whether the Gemini API key is configured.
    if not GEMINI_API_KEY:
        base_context["error"] = (
            "Gemini API key is not configured. "
            "Please check the GEMINI_API_KEY environment variable."
        )

        return render(
            request,
            "generator/results.html",
            base_context,
        )

    # Prompt Gemini to analyze the supplied brand information.
    prompt = f"""
You are BrandVoice AI, an expert social media strategist and copywriter.

Generate exactly 10 original tweets using the information provided below.

BRAND INFORMATION
Brand name: {brand_name}
Industry: {industry}
Campaign objective: {objective}
Products and services: {products}
Target audience: {audience}
Preferred tone: {tone}
Brand description: {brand_description}

BRAND VOICE ANALYSIS
Provide exactly 4 concise observations covering:
1. Brand tone and personality.
2. Audience and communication style.
3. Messaging themes and content direction.
4. Language style and engagement approach.

Infer the brand voice only from the information provided.
Do not claim to have independently analyzed social media accounts.

TWEET VARIETY
Generate 10 distinct tweets with varied purposes:
- 2 conversational or engagement-focused tweets.
- 2 product discovery or promotional tweets.
- 2 informative or value-driven tweets.
- 2 witty, playful, or creative tweets.
- 2 campaign-oriented or community-focused tweets.

Adapt the content to the brand and campaign objective.

QUALITY REQUIREMENTS
- Keep each tweet within the 280-character limit.
- Make all 10 tweets meaningfully different.
- Avoid repetitive openings and ideas.
- Use relevant calls to action when appropriate.
- Do not invent statistics, testimonials, discounts, offers,
  guarantees, or unsupported product claims.
- Ensure all content suits the supplied brand details.
- Return valid JSON only, without Markdown code fences.

OUTPUT FORMAT
Use exactly this structure:
{{
    "voice_summary": [
        "First observation",
        "Second observation",
        "Third observation",
        "Fourth observation"
    ],
    "tweets": [
        {{
            "text": "Tweet text",
            "purpose": "Purpose of the tweet"
        }}
    ]
}}

The voice_summary must contain exactly 4 strings.
The tweets array must contain exactly 10 objects.
Each tweet must contain text and purpose.
"""

    try:
        # Initialize the Gemini client.
        client = genai.Client(
            api_key=GEMINI_API_KEY,
            http_options={"timeout": 60000},
        )

        # Generate content using Gemini.
        response = client.interactions.create(
            model="gemini-3.8-flash",
            input=prompt,
        )

        response_text = (response.output_text or "").strip()

        # Remove Markdown fences if returned unexpectedly.
        response_text = re.sub(
            r"^```(?:json)?\s*|\s*```$",
            "",
            response_text,
            flags=re.IGNORECASE,
        ).strip()

        # Parse the JSON response.
        data = json.loads(response_text)

        generated_summary = data.get("voice_summary")
        generated_tweets = data.get("tweets")

        # Validate the voice summary.
        if not isinstance(generated_summary, list):
            raise ValueError("The AI returned an invalid voice summary.")

        if len(generated_summary) != 4:
            raise ValueError(
                "The AI did not return exactly four voice observations."
            )

        # Validate the tweets list.
        if not isinstance(generated_tweets, list):
            raise ValueError("The AI returned an invalid tweets list.")

        if len(generated_tweets) != 10:
            raise ValueError(
                "The AI did not return exactly 10 tweets. Please try again."
            )

        validated_tweets = []

        for tweet in generated_tweets:
            if not isinstance(tweet, dict):
                raise ValueError("The AI returned an invalid tweet.")

            text = str(tweet.get("text", "")).strip()
            purpose = str(tweet.get("purpose", "")).strip()

            if not text or not purpose:
                raise ValueError(
                    "A generated tweet is missing its text or purpose."
                )

            if len(text) > 280:
                raise ValueError(
                    "A generated tweet exceeds the 280-character limit."
                )

            validated_tweets.append(
                {
                    "text": text,
                    "purpose": purpose,
                }
            )

        # Clean and validate the generated voice observations.
        voice_summary = [
            str(item).strip()
            for item in generated_summary
            if str(item).strip()
        ]

        if len(voice_summary) != 4:
            raise ValueError(
                "The generated brand voice summary is incomplete."
            )

        # Add AI results to the existing brand information.
        context = {
            **base_context,
            "voice_summary": voice_summary,
            "tweets": validated_tweets,
            "generation_mode": "Gemini AI Generated",
        }

        return render(
            request,
            "generator/results.html",
            context,
        )

    except Exception as exc:
        # Log the technical error without exposing credentials.
        print(
            f"BrandVoice AI generation error: "
            f"{type(exc).__name__}: {exc}"
        )

        error_message = (
            "We couldn't generate the tweets right now. "
            "Please try again in a moment."
        )

        error_text = str(exc).lower()

        if (
            "429" in error_text
            or "quota" in error_text
            or "resource_exhausted" in error_text
        ):
            error_message = (
                "The Gemini API request limit has been reached. "
                "Please wait and try again."
            )

        elif (
            "timeout" in error_text
            or "timed out" in error_text
        ):
            error_message = (
                "The AI request took too long. Please try again."
            )

        elif (
            "json" in error_text
            or "invalid" in error_text
        ):
            error_message = (
                "The AI returned an unexpected response. "
                "Please try generating the tweets again."
            )

        base_context["error"] = error_message

        return render(
            request,
            "generator/results.html",
            base_context,
        )

