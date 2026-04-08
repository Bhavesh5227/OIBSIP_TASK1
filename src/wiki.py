import wikipedia
import warnings
warnings.filterwarnings("ignore")   # suppresses the lxml parser warning

def get_wiki(topic):
    try:
        # search first to find the closest matching page title
        search_results = wikipedia.search(topic)
        print(f"DEBUG wiki search results: {search_results}")

        if not search_results:
            return f"I couldn't find any information on {topic}."

        # use the top search result instead of exact topic match
        summary = wikipedia.summary(search_results[0], sentences=3)
        return summary

    except wikipedia.exceptions.DisambiguationError as e:
        options = ", ".join(e.options[:3])
        return f"{topic} is ambiguous. Did you mean: {options}?"

    except wikipedia.exceptions.PageError:
        return f"I couldn't find any information on {topic}."

    except Exception as e:
        print(f"Wiki error: {e}")
        return "Something went wrong fetching Wikipedia."