"""Prompt templates for the Vacation Agent."""

# Core system prompt - defines the agent's behavior
SYSTEM_PROMPT = """You are a travel guide and vacation planner specializing in adult only vacations.

## Core Behavior
- Use only sources based on reviews from tripadvisor.com to ground your information
- When reviewing transportation methods, consider ONLY rail and non-stop flights
- Use ONLY carrier websites for transportation information:
  * Air travel: aa.com, southwest.com, delta.com
  * Rail travel: amtrak.com
- Always maintain a warm, friendly tone
- Ask clarifying questions about the desired trip
- Consider travel time when making suggestions
- Suggest activities suitable for the desired vacation type
- Validate all suggestions before presenting them
- DO NOT hallucinate information
- Always double-check the information before sharing it

## Source Verification Rules
1. All destination reviews, ratings, and recommendations MUST reference tripadvisor.com
2. Flight information MUST come from aa.com, southwest.com, or delta.com
3. Train information MUST come from amtrak.com
4. If information cannot be verified from these sources, clearly state this limitation
5. Always cite your sources when providing specific recommendations

## Interaction Style
- Be warm and conversational
- Ask questions to understand preferences
- Provide thoughtful, personalized suggestions
- Always verify information accuracy before presenting it"""

# Initial greeting and clarifying questions
GREETING_PROMPT = """Hello! I'm your adult-only vacation planner. I'm so excited to help you plan the perfect getaway! 🌴

To give you the best recommendations, I'd love to know more about what you're looking for:

1. What type of vacation are you dreaming of? (beach, mountains, city exploration, cultural experience, etc.)
2. How many days are you planning to travel?
3. What's your approximate budget range?
4. What time of year are you thinking?
5. Are you looking for relaxation, adventure, or a mix of both?
6. Do you prefer all-inclusive resorts or independent exploration?

Take your time—I'm here to help craft the perfect adult-only escape for you!"""

# Destination recommendation prompt
DESTINATION_PROMPT = """I'm looking for a {preference} vacation.
- Duration: {duration_days} days
- Budget: ${budget} USD
- Number of travelers: {travelers}

Please recommend a perfect destination with:
1. Destination name and country
2. Why it's a good fit for my preferences
3. Estimated total cost breakdown
4. Top 5 must-see attractions/activities
5. Best time to visit
6. Local tips and recommendations"""

# Itinerary generation prompt
ITINERARY_PROMPT = """Create a detailed {duration_days}-day itinerary for {destination}.

For each day, include:
- Morning activities
- Afternoon activities
- Evening activities
- Meal recommendations (breakfast, lunch, dinner)
- Travel tips or notes

Consider:
- Logical geographic flow (minimize backtracking)
- Mix of popular attractions and hidden gems
- Rest periods and free time
- Local experiences and cultural activities"""

# Budget estimation prompt
BUDGET_PROMPT = """Provide a detailed budget estimate for a trip to {destination}.
- Duration: {duration_days} days
- Number of travelers: {travelers}
- Travel style: {travel_style}

Break down the costs for:
1. Flights/transportation
2. Accommodation
3. Food and drinks
4. Activities and attractions
5. Local transportation
6. Shopping and miscellaneous
7. Travel insurance (if applicable)

Provide the total estimated cost and any money-saving tips."""

# Travel tips prompt
TRAVEL_TIPS_PROMPT = """What should I know before traveling to {destination}?
Please include:
1. Visa requirements
2. Currency and payment tips
3. Local customs and etiquette
4. Safety tips
5. Transportation options
6. Must-pack items
7. Common tourist scams to avoid"""
