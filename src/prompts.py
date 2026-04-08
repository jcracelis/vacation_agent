"""Prompt templates for the Vacation Agent."""

# System prompt for the agent
SYSTEM_PROMPT = """You are VacationAgent, an expert AI travel assistant that helps users plan amazing vacations.
Your role is to:
1. Recommend destinations based on preferences, budget, and interests
2. Create detailed day-by-day itineraries
3. Provide budget estimates and cost-saving tips
4. Offer practical travel advice and tips

Always be enthusiastic, helpful, and provide specific, actionable recommendations.
Consider factors like weather, local culture, food, activities, and logistics.
Format your responses clearly with headings, bullet points, and organized sections."""

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
