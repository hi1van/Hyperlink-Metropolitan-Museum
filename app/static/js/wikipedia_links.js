async function fetchWikipediaLink(query) {
    const apiUrl = `https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(query)}`;
    try {
        const response = await fetch(apiUrl);
        if (response.ok) {
            const data = await response.json();
            if (data.type !== "disambiguation") {
                return {
                    link: data.content_urls.desktop.page || null, // get the Wikipedia page URL
                    extract: data.extract || null   // get the extract or default message
                };
            }
        }
    } catch (error) {
        console.error("Error fetching Wikipedia link:", error);
    }
    return { link: null, extract: null }; // return null if no valid link is found
}