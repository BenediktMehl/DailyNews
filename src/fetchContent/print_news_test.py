import requests

def print_news():
    api_url = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
    response = requests.get(api_url)
    top_story_ids = response.json()[:3]  # Get top 3 story IDs

    for story_id in top_story_ids:
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json?print=pretty"
        story_response = requests.get(story_url)
        story_data = story_response.json()
        print(f"Title: {story_data.get('title')}")
        print(f"URL: {story_data.get('url')}")
        print(f"Score: {story_data.get('score')}")
        print(f"By: {story_data.get('by')}")
        print(f"Time: {story_data.get('time')}")
        print(f"Descendants: {story_data.get('descendants')}")
        print("-" * 40)

if __name__ == '__main__':
    print_news()
