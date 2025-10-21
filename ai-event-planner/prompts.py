from typing import Dict

def build_system_prompt() -> str:
    return (
        "You are a senior event producer and logistics planner. "
        "Deliver detailed, actionable event plans that strictly follow this section order:\n"
        "1) Event Details (Event type, Guest Count, Budget, Theme/Style, Duration, Special Considerations)\n"
        "2) Timeline of Preparation (Planning phase → Final week/day tasks)\n"
        "3) Suggested Activities/Entertainment (age/audience‑appropriate)\n"
        "4) Food and Drinks Suggestions (meals, snacks, drinks, note dietary needs)\n"
        "5) Venue and Decoration Ideas (layout + theme‑aligned décor)\n"
        "6) Backup options (weather, vendor fallback, timing contingencies)\n\n"
        "Constraints:\n"
        "- Keep the plan coherent with the stated budget; include rough cost allocations where useful.\n"
        "- Use clear bullet points and subheadings; prefer concise, operative language.\n"
        "- Include at least 3 concrete vendor‑agnostic action items per section.\n"
    )

def build_few_shot_examples():
    # Two concise shots to shape tone/structure
    ex1 = {
        "role": "user",
        "parts": [format_user_brief({
            "event_type": "Picnic",
            "guest_count": 10,
            "budget": 200,
            "theme": "Cottagecore",
            "duration": "3 hours",
            "special_considerations": "park setting; shade preferred; vegetarian options"
        })]
    }
    ex1_out = {
        "role": "model",
        "parts": ["""
# Event Details
- **Event Type:** Picnic
- **Guest Count:** 10
- **Budget:** $200
- **Theme/Style:** Cottagecore
- **Duration:** 3 hours
- **Special Considerations:** Park setting; shade preferred; vegetarian options

## Timeline of Preparation
**Planning (2–3 weeks out)**
- Define picnic area layout; verify park rules; secure shade via canopy or trees.
- Menu draft with vegetarian focus; assign shopping & prep tasks.
- Create a shared list for blankets, baskets, ice packs.

**Final week/day**
- Purchase perishables; pre‑chill drinks; confirm weather & backup gazebo.
- Prep finger foods; pack utensils, wipes, trash bags.
- Arrive 45–60 min early to stage blankets & décor.

## Suggested Activities/Entertainment
- Low‑key lawn games (ring toss, cards); nature sketching mini‑kit.
- Curated acoustic playlist; optional poetry or story circle.
- Photo scavenger list themed around flowers & textures.

## Food and Drinks Suggestions
- Sandwich minis (caprese, hummus‑veg); fruit skewers; cheese & crackers.
- Lemonade, iced tea, sparkling water; one thermos of herbal tea.
- Label allergens; pack gluten‑free crackers and dairy‑free dip.

## Venue and Decoration Ideas
- Layout: 2–3 blankets in a U‑shape; low crates as tables; basket centerpieces.
- Décor: gingham cloths, wildflower jars, twine tags; soft neutrals & greens.
- Shade: place under trees or pop‑up canopy; clip cloth for side shade.

## Backup options
- In case of wind: weighted clips for cloths, sealed containers.
- In case of light rain: nearby gazebo; shift to sheltered picnic tables.
- In case of heat: earlier start; misting spray; extra ice for drinks.
"""]
    }

    ex2 = {
        "role": "user",
        "parts": [format_user_brief({
            "event_type": "Pool Party",
            "guest_count": 50,
            "budget": 500,
            "theme": "4th of July",
            "duration": "4 hours",
            "special_considerations": "outdoors; safety supervision; simple DIY décor"
        })]
    }
    ex2_out = {
        "role": "model",
        "parts": ["""
# Event Details
- **Event Type:** Pool Party
- **Guest Count:** 50
- **Budget:** $500
- **Theme/Style:** 4th of July (casual & festive)
- **Duration:** 4 hours
- **Special Considerations:** Outdoors; safety supervision; DIY décor

## Timeline of Preparation
**Planning (3–4 weeks out)**
- Safety: identify adult swim monitors; print rules; stock sunscreen & first‑aid.
- Budget split: ~40% food, 20% drinks/ice, 15% décor, 15% activities, 10% misc.
- Obtain music device + waterproof speaker; outline playlist segments.

**Final week/day**
- Grocery run for grillables & sides; fill coolers with ice.
- Prep signage (restrooms, no‑running); set up shade & towel station.
- Test lighting for evening; gather trash & recycling bins.

## Suggested Activities/Entertainment
- Cannonball contest; relay race with pool noodles; beach‑ball volleyball.
- Photo backdrop with red/white/blue streamers; instant camera props.
- Optional: simple fireworks‑free light show with glow sticks after sunset.

## Food and Drinks Suggestions
- Grill: hot dogs & veggie skewers; pasta salad; corn on the cob.
- Red/white/blue fruit tray; popsicles in cooler; chips & salsa.
- Drinks: water, lemonade, iced tea; coolers labeled; BYOB rules posted.

## Venue and Decoration Ideas
- Layout: shade zone (canopies), food buffet near outlet, games end opposite quiet lounge.
- Décor: bunting, paper fans, reusable flags; color‑blocked tablecloths.
- Lighting: string lights along fence; battery lanterns near seating.

## Backup options
- Bad weather: move to community room; keep cold foods in coolers; shift games to trivia/charades.
- Equipment failure: backup Bluetooth speaker; spare extension cords.
- Food shortage: frozen pizzas & extra chips as reserve.
"""]
    }

    return [ex1, ex1_out, ex2, ex2_out]

def format_user_brief(brief: Dict) -> str:
    return (
        "# New Event Brief\n"
        f"Event Type: {brief.get('event_type','')}\n"
        f"Guest Count: {brief.get('guest_count','')}\n"
        f"Budget: ${brief.get('budget','')}\n"
        f"Theme/Style: {brief.get('theme','')}\n"
        f"Duration: {brief.get('duration','')}\n"
        f"Special Considerations: {brief.get('special_considerations','')}\n\n"
        "Please generate a fully structured plan following the required sections."
    )
