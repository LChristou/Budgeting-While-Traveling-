
"""Travel Budget Buddy: interactive college-friendly trip budget planner."""

from dataclasses import dataclass, field
import math
from drafter import *

set_website_title("Budget Traveler")
set_site_information(
    author="Lazo Christou",
    description="Calculates vacation budget; helps stay within range",
    sources="Thanks to the Drafter docs and Ai.",
    planning=["CS1 Final Project 0_ Pick a Problem.pdf", "CS1 Final Project 1_ Design.pdf", "Ai Conversation (Coding Project).pdf"],
    links=["https://github.com/LChristou/Budgeting-While-Traveling-/blob/main/CS1%20Final%20Project%200_%20Pick%20a%20Problem.pdf",
           "https://github.com/LChristou/Budgeting-While-Traveling-/blob/main/CS1%20Final%20Project%201_%20Design.pdf", 
          "https://github.com/LChristou/Budgeting-While-Traveling-/blob/main/Ai%20Conversation%20(Coding%20Project).pdf"]
)
hide_debug_information()
set_website_framed(False)

@dataclass
class Activity:
    """Remember the name, category, and estimated cost of a trip activity."""
    name: str
    category: str
    cost: float


@dataclass
class Place:
    """Describe a curated destination idea with an illustrative allowance."""
    name: str
    category: str
    cost: float
    description: str


@dataclass
class State:
    """Remember editable trip details while the visitor moves between pages."""
    destination: str = ""
    budget: float = 0.0
    days: int = 0
    activities: list[Activity] = field(default_factory=list)
    transportation: float = 0.0
    accommodations: float = 0.0
    food: float = 0.0
    interest: str = "All"
    max_suggestion: float = 50.0
    trip_notes: str = ""
    message: str = ""


def dollars(amount: float) -> str:
    """Format a number of dollars with two decimal places."""
    return "$" + format(amount, ".2f")


def is_amount(text: str) -> bool:
    """Accept only nonnegative, finite numerical text."""
    try:
        amount = float(text)
        return math.isfinite(amount) and amount >= 0
    except ValueError:
        return False


def activities_cost(state: State) -> float:
    """Add activity prices using a loop over Activity instances."""
    total = 0.0
    for activity in state.activities:
        total = total + activity.cost
    return total


def total_cost(state: State) -> float:
    """Calculate the full trip total without double-counting food ideas."""
    return (state.transportation + state.accommodations +
            state.food + activities_cost(state))


def money_left(state: State) -> float:
    """Find how much of the overall budget is not allocated."""
    return state.budget - total_cost(state)


def daily_food_budget(state: State) -> float:
    """Calculate the average food allowance for one day of travel."""
    if state.days <= 0:
        return 0.0
    return state.food / state.days


def budget_status(state: State) -> str:
    """Describe whether estimated spending is over or under the budget."""
    if state.budget <= 0:
        return "Please create a trip with a positive budget first."
    if money_left(state) < 0:
        return "Over budget by " + dollars(-money_left(state)) + "."
    if money_left(state) == 0:
        return "Exactly on budget."
    return "Within budget! You have " + dollars(money_left(state)) + " left."


def menu() -> list:
    """Build navigation links for the six main pages."""
    return [HorizontalRule(), Link("Home", "index"),
            Link("Trip Setup", "trip_page"),
            Link("Activities", "activities_page"),
            Link("Expenses", "expenses_page"),
            Link("Explore", "explore_page"),
            Link("Summary", "summary_page")]


def show_activities(state: State) -> list:
    """Display the list of activities in the order they were added."""
    content = []
    if len(state.activities) == 0:
        content.append(Paragraph("No activities planned yet."))
    else:
        for activity in state.activities:
            content.append(Paragraph(activity.name + " (" + activity.category +
                                     ") - " + dollars(activity.cost)))
    return content


def destination_key(destination: str) -> str:
    """Identify one of the destinations with built-in suggestions."""
    name = destination.strip().lower()
    for city in ["rome", "athens", "paris", "london", "milan"]:
        if city in name:
            return city
    return ""


def places_for(destination: str) -> list[Place]:
    """Return sample local ideas, NOT real-time prices or availability.

    Food prices are illustrative per-person meal allowances; shopping entries
    cost $0 because browsing is free, but purchases must be budgeted separately.
    """
    city = destination_key(destination)
    if city == "rome":
        return [
            Place("Mercato Testaccio", "Food", 15,
                  "Casual market food; check current menus before visiting."),
            Place("Trastevere pizza stop", "Food", 18,
                  "Look for a casual pizza place in this neighborhood."),
            Place("Via del Corso", "Shopping", 0,
                  "Browse fashion and accessories; purchases are extra."),
            Place("Porta Portese market", "Shopping", 0,
                  "Browse market stalls; check the market schedule."),
            Place("Trevi Fountain walk", "Sightseeing", 0,
                  "Enjoy the surrounding streets; access charges may apply."),
            Place("Museum allowance", "Museums", 22,
                  "Set money aside for admission; verify actual ticket prices.")]
    if city == "athens":
        return [
            Place("Central Market food stop", "Food", 12,
                  "Look for a simple meal near Varvakios Market."),
            Place("Souvlaki lunch", "Food", 10,
                  "Estimate a casual lunch; restaurant prices vary."),
            Place("Ermou Street", "Shopping", 0,
                  "Browse fashion shops; purchases are extra."),
            Place("Monastiraki market area", "Shopping", 0,
                  "Browse souvenirs and secondhand items; purchases are extra."),
            Place("Plaka neighborhood walk", "Sightseeing", 0,
                  "Walk historic streets and browse public squares."),
            Place("Museum allowance", "Museums", 20,
                  "A sample entry allowance; check actual admission prices.")]
    if city == "paris":
        return [
            Place("Bakery lunch", "Food", 14,
                  "Budget for a pastry or sandwich from a local bakery."),
            Place("Picnic supplies", "Food", 16,
                  "Try a grocery-store picnic to save money."),
            Place("Rue de Rivoli", "Shopping", 0,
                  "Browse popular shopping streets; purchases are extra."),
            Place("Le Marais boutiques", "Shopping", 0,
                  "Window-shop independent stores; purchases are extra."),
            Place("Tuileries Garden walk", "Sightseeing", 0,
                  "Plan a public-garden stroll."),
            Place("Museum allowance", "Museums", 25,
                  "A planning amount, not a quoted museum ticket price.")]
    if city == "london":
        return [
            Place("Borough Market food stop", "Food", 18,
                  "Explore food stalls; check vendor prices."),
            Place("Camden Market food stop", "Food", 15,
                  "Consider an informal street-food meal."),
            Place("Camden Market shops", "Shopping", 0,
                  "Browse stalls and vintage clothing; purchases are extra."),
            Place("Covent Garden", "Shopping", 0,
                  "Browse stores and market stalls; purchases are extra."),
            Place("Thames riverside walk", "Sightseeing", 0,
                  "Enjoy a walk along the river."),
            Place("Museum allowance", "Museums", 15,
                  "Some collections are free; check special exhibit fees.")]
    if city == "milan":
        return [
            Place("Casual cafe lunch", "Food", 16,
                  "Estimate a simple cafe lunch; prices vary."),
            Place("Pizza slice stop", "Food", 10,
                  "Try a quick inexpensive meal."),
            Place("Corso Buenos Aires", "Shopping", 0,
                  "Browse many high-street shops; purchases are extra."),
            Place("Corso Vittorio Emanuele II", "Shopping", 0,
                  "Explore central stores; purchases are extra."),
            Place("Duomo square walk", "Sightseeing", 0,
                  "Explore the square; cathedral admission may cost extra."),
            Place("Museum allowance", "Museums", 20,
                  "Budget for admission; check actual current prices.")]
    return []


def interested_places(state: State) -> list[Place]:
    """Filter the destination catalog by interest and maximum sample cost."""
    matches = []
    for place in places_for(state.destination):
        interest_ok = (state.interest == "All" or
                       place.category == state.interest)
        if interest_ok and place.cost <= state.max_suggestion:
            matches.append(place)
    return matches


def money_tips(state: State) -> list:
    """Suggest realistic ways to adjust a trip estimate."""
    tips = []
    if state.days > 0 and daily_food_budget(state) < 25:
        tips.append(Paragraph("Food tip: Your daily food allowance is below "
                              "$25. Consider markets, groceries, or simple meals."))
    if state.budget > 0 and state.accommodations > state.budget * 0.5:
        tips.append(Paragraph("Accommodation tip: Your lodging takes over "
                              "half the budget. Compare less expensive options."))
    if money_left(state) < 0:
        tips.append(Paragraph("Savings tip: Reduce a planned activity or "
                              "revisit transportation and lodging estimates."))
    if len(state.activities) == 0:
        tips.append(Paragraph("Planning tip: Add activities so their costs "
                              "appear in your total."))
    if len(tips) == 0:
        tips.append(Paragraph("Your estimates look organized. Remember to "
                              "leave some money for unexpected expenses."))
    return tips


@route
def index(state: State) -> Page:
    """Show the home page and explain the planner's purpose."""
    return Page(state, [
        Header("Travel Budget Buddy"),
        Paragraph("Plan a vacation that fits your budget."),
        Paragraph("Create a trip, enter expenses, find city-specific ideas, "
                  "and see what you can afford."),
        Paragraph("Recommendations are prewritten examples, not live booking data."),
        Button("Start Planning", "trip_page")
    ] + menu())


@route
def trip_page(state: State) -> Page:
    """Show fields for destination, budget, and trip duration."""
    return Page(state, [
        Header("1. Trip Setup"), Paragraph(state.message),
        Paragraph("Where are you going?"),
        TextBox("destination", state.destination, placeholder="Rome, Italy"),
        Paragraph("Total budget in USD"),
        TextBox("budget_text", str(state.budget), kind="number"),
        Paragraph("Number of travel days"),
        TextBox("days_text", str(state.days), kind="number"),
        Button("Save Trip", "save_trip")
    ] + menu())


@route
def save_trip(state: State, destination: str,
              budget_text: str, days_text: str) -> Page:
    """Save trip details only when all three entries are valid."""
    if destination.strip() == "":
        state.message = "Enter a destination first."
        return trip_page(state)
    if not is_amount(budget_text) or float(budget_text) <= 0:
        state.message = "Enter a budget above zero."
        return trip_page(state)
    try:
        days = int(days_text)
    except ValueError:
        state.message = "Days must be a whole number."
        return trip_page(state)
    if days <= 0:
        state.message = "Travel days must be greater than zero."
        return trip_page(state)
    state.destination = destination.strip()
    state.budget = float(budget_text)
    state.days = days
    state.message = "Trip saved! Add activities next."
    return activities_page(state)


@route
def activities_page(state: State) -> Page:
    """Show saved activities and a form for another activity."""
    return Page(state, [
        Header("2. Plan Activities"), Paragraph(state.message),
        Header("Your Activities", 3)
    ] + show_activities(state) + [
        Paragraph("Activity name"),
        TextBox("activity_name", "", placeholder="e.g. Shopping"),
        Paragraph("Category"),
        SelectBox("category", ["Shopping", "Food", "Museums",
                               "Sightseeing", "Other"]),
        Paragraph("Estimated cost in USD"),
        TextBox("cost_text", "0", kind="number"),
        Button("Add Activity", "add_activity"),
        Button("Remove Last Activity", "remove_activity"),
        Button("Get Local Suggestions", "explore_page"),
        Paragraph("Activity total: " + dollars(activities_cost(state))),
        Paragraph("Meals already included in your Food expense should not "
                  "be added again as activities.")
    ] + menu())


@route
def add_activity(state: State, activity_name: str,
                 category: str, cost_text: str) -> Page:
    """Validate and add a new Activity instance to State."""
    if activity_name.strip() == "":
        state.message = "Enter an activity name."
        return activities_page(state)
    if not is_amount(cost_text):
        state.message = "Enter a valid nonnegative activity cost."
        return activities_page(state)
    state.activities.append(Activity(activity_name.strip(), category,
                                     float(cost_text)))
    if category in ["Shopping", "Food", "Museums", "Sightseeing"]:
        state.interest = category
    state.message = "Activity saved! Your suggestions now reflect your interests."
    return activities_page(state)


@route
def remove_activity(state: State) -> Page:
    """Undo the most recent activity without changing other trip details."""
    if len(state.activities) == 0:
        state.message = "There is no activity to remove."
    else:
        removed = state.activities.pop()
        state.message = "Removed " + removed.name + "."
    return activities_page(state)


@route
def expenses_page(state: State) -> Page:
    """Show the main spending categories and stored amounts."""
    return Page(state, [
        Header("3. Estimate Expenses"), Paragraph(state.message),
        Paragraph("Enter totals for the ENTIRE trip, not daily costs."),
        Paragraph("Transportation ($)"),
        TextBox("transport_text", str(state.transportation), kind="number"),
        Paragraph("Accommodation ($)"),
        TextBox("hotel_text", str(state.accommodations), kind="number"),
        Paragraph("Food ($)"),
        TextBox("food_text", str(state.food), kind="number"),
        Button("Save Expenses", "save_expenses")
    ] + menu())


@route
def save_expenses(state: State, transport_text: str,
                  hotel_text: str, food_text: str) -> Page:
    """Validate and save transportation, hotel, and food spending."""
    if (not is_amount(transport_text) or
            not is_amount(hotel_text) or not is_amount(food_text)):
        state.message = "Enter valid nonnegative numbers for all expenses."
        return expenses_page(state)
    state.transportation = float(transport_text)
    state.accommodations = float(hotel_text)
    state.food = float(food_text)
    state.message = "Expenses saved. Review your trip suggestions!"
    return explore_page(state)


@route
def explore_page(state: State) -> Page:
    """Show personalized ideas filtered by location, interest, and allowance."""
    if state.destination == "":
        return Page(state, [Header("4. Explore Your Destination"),
                            Paragraph("Set up a trip first."),
                            Button("Trip Setup", "trip_page")] + menu())
    items = [
        Header("4. Explore " + state.destination),
        Paragraph(state.message),
        Paragraph("Choose the kind of place you want to explore."),
        SelectBox("chosen_interest", ["All", "Food", "Shopping",
                                     "Museums", "Sightseeing"], state.interest),
        Paragraph("Maximum sample cost per suggestion ($)"),
        TextBox("limit_text", str(state.max_suggestion), kind="number"),
        Button("Update Suggestions", "filter_places"),
        Paragraph("Food budget per day: " + dollars(daily_food_budget(state))),
        Paragraph("Money not yet allocated: " + dollars(money_left(state))),
        Paragraph("Prices below are example planning allowances, NOT live prices."),
        Paragraph("A $0 shopping suggestion means browsing is free; "
                  "buying items is not."),
        Header("Ideas for You", 2)
    ]
    if destination_key(state.destination) == "":
        items.append(Paragraph("No built-in city guide exists for this destination. "
                               "Try a food market, a shopping district, or a free "
                               "walking route, and enter actual costs yourself."))
    else:
        matches = interested_places(state)
        if len(matches) == 0:
            items.append(Paragraph("No ideas match that filter. Try All or a "
                                   "higher maximum cost."))
        for place in matches:
            items.append(Header(place.name + " - " + place.category, 3))
            items.append(Paragraph(place.description))
            items.append(Paragraph("Sample cost: " + dollars(place.cost)))
            if place.category == "Food" and state.days > 0:
                if place.cost <= daily_food_budget(state):
                    items.append(Paragraph("Within your average daily food allowance."))
                else:
                    items.append(Paragraph("Above your average daily food allowance."))
            elif place.cost > money_left(state):
                items.append(Paragraph("This could put your trip over budget."))
            items.append(HorizontalRule())
    return Page(state, items + [
        Paragraph("Add any places you choose on the Activities page. "
                  "For meals, use the Food budget instead of double-counting."),
        Button("Add an Activity", "activities_page"),
        Button("See My Summary", "summary_page")
    ] + menu())


@route
def filter_places(state: State, chosen_interest: str,
                  limit_text: str) -> Page:
    """Save the chosen interest and spending limit for suggestions."""
    if not is_amount(limit_text):
        state.message = "Enter a valid maximum suggestion cost."
        return explore_page(state)
    state.interest = chosen_interest
    state.max_suggestion = float(limit_text)
    state.message = "Suggestions updated for " + chosen_interest + "."
    return explore_page(state)


@route
def summary_page(state: State) -> Page:
    """Display a trip breakdown, budget comparison, and saving tips."""
    return Page(state, [
        Header("5. Your Trip Summary"),
        Paragraph("Destination: " + (state.destination or "Not chosen")),
        Paragraph("Travel days: " + str(state.days)),
        Paragraph("Trip budget: " + dollars(state.budget)),
        Header("Spending Breakdown", 3),
        Paragraph("Transportation: " + dollars(state.transportation)),
        Paragraph("Accommodation: " + dollars(state.accommodations)),
        Paragraph("Food: " + dollars(state.food)),
        Paragraph("Activities: " + dollars(activities_cost(state))),
        Header("Total: " + dollars(total_cost(state)), 2),
        Paragraph(budget_status(state)),
        Header("Average Costs", 3),
        Paragraph("Daily food budget: " + dollars(daily_food_budget(state))),
        Header("Your Planned Activities", 3)
    ] + show_activities(state) + [
        Header("Budget Tips", 3)
    ] + money_tips(state) + [
        Header("Trip Notes", 3),
        TextArea("notes_text", state.trip_notes),
        Button("Save Notes", "save_notes"),
        Button("Explore More Places", "explore_page"),
        Button("Start a New Trip", "reset_trip")
    ] + menu())


@route
def save_notes(state: State, notes_text: str) -> Page:
    """Remember user-written trip notes in State."""
    state.trip_notes = notes_text
    state.message = "Notes saved for this planning session."
    return summary_page(state)


@route
def reset_trip(state: State) -> Page:
    """Clear trip information and return to the welcome page."""
    state.destination = ""
    state.budget = 0.0
    state.days = 0
    state.activities = []
    state.transportation = 0.0
    state.accommodations = 0.0
    state.food = 0.0
    state.interest = "All"
    state.max_suggestion = 50.0
    state.trip_notes = ""
    state.message = "Previous trip cleared."
    return index(state)


# Testing is kept in its own function so it can be explained to the TA.
# Each route has a test; assertions check important changes in State.
def run_tests() -> None:
    """Test all routes and main calculations before starting Drafter."""
    assert_has(index(State()), "Travel Budget Buddy")
    assert_has(trip_page(State()), "Trip Setup")
    assert_has(activities_page(State()), "Plan Activities")
    assert_has(expenses_page(State()), "Estimate Expenses")
    assert_has(explore_page(State()), "Set up a trip first")
    assert_has(summary_page(State()), "Your Trip Summary")

    trip = State()
    assert_has(save_trip(trip, "Rome", "700", "4"), "Plan Activities")
    assert_equal(trip.destination, "Rome")
    assert_equal(trip.days, 4)
    assert_has(save_trip(State(), "Rome", "-3", "2"), "budget above zero")
    assert_has(save_trip(State(), "Paris", "200", "abc"), "whole number")

    assert_has(add_activity(trip, "Shopping", "Shopping", "30"), "Shopping")
    assert_equal(activities_cost(trip), 30.0)
    assert_equal(trip.interest, "Shopping")
    assert_has(remove_activity(trip), "Removed Shopping")
    assert_equal(len(trip.activities), 0)

    assert_has(save_expenses(trip, "120", "300", "100"), "Explore Rome")
    assert_equal(total_cost(trip), 520.0)
    assert_equal(daily_food_budget(trip), 25.0)
    assert_has(save_expenses(trip, "nope", "30", "20"),
               "valid nonnegative numbers")
    trip.interest = "All"
    assert_has(explore_page(trip), "Mercato Testaccio")
    assert_has(filter_places(trip, "Shopping", "10"), "Via del Corso")
    assert_equal(trip.interest, "Shopping")
    assert_has(filter_places(trip, "Food", "bad"), "valid maximum")
    assert_has(explore_page(State(destination="Oslo", budget=200, days=3)),
               "No built-in city guide")
    assert_has(summary_page(State(destination="Rome", budget=20,
                                  days=2, food=30)), "Over budget")
    assert_has(save_notes(trip, "Remember passport"), "Remember passport")
    assert_equal(trip.trip_notes, "Remember passport")
    assert_has(reset_trip(trip), "Travel Budget Buddy")
    assert_equal(trip.budget, 0.0)
    assert_equal(len(trip.activities), 0)


set_website_title("Travel Budget Buddy")
set_website_style("water")
set_site_information(
    "Lazo Christou",
    "Student-friendly trip planner with budgeting and curated city ideas.",
    "Drafter documentation: https://drafter-edu.github.io/drafter/",
    "See Final Project 0 and Final Project 1 worksheets in this repository.",
    []
)
# Uncomment this when the website is ready for a public demonstration.
# hide_debug_information()

run_tests()
start_server(State())

