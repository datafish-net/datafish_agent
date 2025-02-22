require('dotenv').config();
const express = require('express');
const axios = require('axios');
const OpenAI = require('openai');

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 3000;
const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY
});

async function fetchWebContent(url) {
    try {
        console.log('Fetching URL:', url);
        const response = await axios.get(url, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        });
        console.log('Response status:', response.status);
        console.log('Response data length:', response.data?.length);
        console.log('First 500 chars of response:', response.data?.substring(0, 500));
        return response.data;
    } catch (error) {
        console.error('Fetch error:', {
            message: error.message,
            status: error.response?.status,
            statusText: error.response?.statusText,
            headers: error.response?.headers
        });
        throw new Error(`Failed to fetch webpage: ${error.message}`);
    }
}

async function extractContentWithGPT(html) {
    try {
        // Truncate HTML to a reasonable length (about 12k chars)
        const truncatedHtml = html.length > 12000 ? html.substring(0, 12000) + '...' : html;
        
        console.log('Sending to GPT, HTML length:', truncatedHtml.length);
        const completion = await openai.chat.completions.create({
            model: "gpt-4o-mini",
            messages: [
                {
                    role: "system",
                    content: "Extract the main content from HTML while removing all HTML tags. Focus on the article/documentation content, headings, and lists. Ignore navigation, footers, and other UI elements."
                },
                {
                    role: "user",
                    content: truncatedHtml
                }
            ],
            temperature: 0.3,
            max_tokens: 4000,
            top_p: 1,
            frequency_penalty: 0,
            presence_penalty: 0
        });

        console.log('GPT response:', completion.choices[0].message.content.substring(0, 200));
        return completion.choices[0].message.content;
    } catch (error) {
        console.error('GPT error:', error);
        throw new Error(`GPT processing failed: ${error.message}`);
    }
}

app.post('/extract', async (req, res) => {
    try {
        const { url } = req.body;
        
        if (!url) {
            return res.status(400).json({ error: 'URL is required' });
        }

        console.log('Processing request for URL:', url);
        const htmlContent = await fetchWebContent(url);
        const cleanContent = await extractContentWithGPT(htmlContent);

        res.json({
            content: cleanContent
        });

    } catch (error) {
        console.error('Error details:', {
            message: error.message,
            url: req.body.url,
            stack: error.stack
        });
        
        res.status(500).json({
            error: 'Failed to extract content',
            message: error.message,
            url: req.body.url
        });
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
}); 