require('dotenv').config();
const express = require('express');
const { chromium } = require('playwright');
const OpenAI = require('openai');
const fs = require('fs').promises;

// Add initialization function
async function initializePlaywright() {
    try {
        console.log('Installing Playwright browsers...');
        const { execSync } = require('child_process');
        execSync('npx playwright install chromium', { stdio: 'inherit' });
        console.log('Playwright browsers installed successfully');
    } catch (error) {
        console.error('Failed to install Playwright browsers:', error);
        process.exit(1);
    }
}

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 3000;
const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY
});

async function fetchWebContent(url) {
    try {
        console.log('Fetching URL:', url);
        const browser = await chromium.launch({ headless: true });
        const page = await browser.newPage();
        
        // Set longer timeouts for the entire page operation
        page.setDefaultTimeout(120000); // 2 minutes
        page.setDefaultNavigationTimeout(120000);

        // Navigate to the page and wait for network to be idle
        await page.goto(url, { 
            waitUntil: 'networkidle',
            timeout: 120000 
        });

        // Wait for dynamic content to load
        await page.waitForLoadState('networkidle', { timeout: 60000 });

        // Scroll to bottom to trigger lazy loading
        await autoScroll(page);

        // Optional: wait a bit more for any final dynamic updates
        await page.waitForTimeout(5000);

        const html = await page.content();
        await browser.close();
        
        console.log('Response data length:', html?.length);
        console.log('First 500 chars of response:', html?.substring(0, 500));
        return html;
    } catch (error) {
        console.error('Fetch error:', {
            message: error.message,
        });
        throw new Error(`Failed to fetch webpage: ${error.message}`);
    }
}

// Helper function to scroll the page
async function autoScroll(page) {
    await page.evaluate(async () => {
        await new Promise((resolve) => {
            let totalHeight = 0;
            const distance = 100;
            const timer = setInterval(() => {
                const scrollHeight = document.body.scrollHeight;
                window.scrollBy(0, distance);
                totalHeight += distance;

                if (totalHeight >= scrollHeight) {
                    clearInterval(timer);
                    resolve();
                }
            }, 100);
        });
    });
}

async function extractApiContent(page) {
    const content = await page.evaluate(() => {
        // Remove unnecessary elements
        const removeSelectors = [
            'header', 'footer', 'nav', '.navigation', '.sidebar',
            'script', 'style', '.cookie-banner', '.announcement',
            '.marketing-section', '.ads', '#hubspot-messages-iframe-container',
            '.search-box', '.menu', '.social-links'
        ];
        
        removeSelectors.forEach(selector => {
            document.querySelectorAll(selector).forEach(el => el.remove());
        });

        // Get the main content
        const mainContent = document.querySelector('main, article, [role="main"], .main-content');
        return mainContent ? mainContent.textContent : document.body.textContent;
    });
    
    return content;
}

async function extractContentWithGPT(content) {
    try {
        const completion = await openai.chat.completions.create({
            model: "gpt-4o-mini",
            messages: [
                {
                    role: "system",
                    content: "You are an API documentation analyzer. Given the content of a documentation page, provide a clear and concise summary that includes: 1) The main purpose/functionality described 2) Key API endpoints or features 3) Important parameters or requirements 4) Any notable limitations or considerations. Focus on technical details and practical usage. If the content is not API-related, provide a general summary of the technical documentation."
                },
                {
                    role: "user",
                    content: content
                }
            ],
            temperature: 0.3,
            max_tokens: 1000
        });
        
        return completion.choices[0].message.content;
    } catch (error) {
        console.error('GPT analysis error:', error);
        return "Failed to analyze content with GPT";
    }
}

// Add this function to extract URLs from HTML
function extractUrls(html, baseUrl) {
    const urlPattern = /<a[^>]+href=["']([^"']+)["'][^>]*>([^<]*)<\/a>/g;
    const urls = [];
    let match;

    // Extract domain from the base URL
    const domain = new URL(baseUrl).origin;

    while ((match = urlPattern.exec(html)) !== null) {
        const [_, url, text] = match;
        // Only add if it's a valid URL and not an anchor
        if (url && !url.startsWith('#')) {
            let fullUrl = url.trim();
            
            // Handle relative URLs
            if (url.startsWith('/')) {
                // For paths starting with '/'
                fullUrl = `${domain}${url}`;
            } else if (!url.startsWith('http')) {
                // For other relative paths
                fullUrl = `${domain}/${url}`;
            }

            urls.push({
                url: fullUrl,
                text: text.trim()
            });
        }
    }

    return urls;
}

// Modify the extract endpoint to crawl all URLs
app.post('/extract', async (req, res) => {
    try {
        const { url } = req.body;
        
        if (!url) {
            return res.status(400).json({ error: 'URL is required' });
        }

        console.log('Processing request for URL:', url);
        const browser = await chromium.launch({ headless: true });
        const page = await browser.newPage();
        
        // Get initial page content and URLs
        const htmlContent = await fetchWebContent(url);
        const urlsContent = extractUrls(htmlContent, url);
        
        // Add main URL as the first entry
        urlsContent.unshift({
            url: url,
            text: 'Main Page'
        });
        
        // Create knowledge pool content
        let knowledgePool = `API Documentation Overview\nMain URL: ${url}\n\n`;
        
        // Process each URL
        console.log(`Found ${urlsContent.length} URLs to process`);
        for (const [index, urlData] of urlsContent.entries()) {
            try {
                console.log(`Processing ${index + 1}/${urlsContent.length}: ${urlData.url}`);
                await page.goto(urlData.url, { waitUntil: 'networkidle' });
                
                // First clean the content
                const cleanContent = await extractApiContent(page);
                
                // Then analyze with GPT
                const analysis = await extractContentWithGPT(cleanContent);
                
                // Add to knowledge pool
                knowledgePool += `\n=== ${urlData.text} ===\nURL: ${urlData.url}\n\n`;
                knowledgePool += `Content Analysis:\n${analysis}\n\n`;
                knowledgePool += `${'='.repeat(80)}\n\n`;
                
            } catch (error) {
                console.error(`Failed to process URL: ${urlData.url}`, error.message);
                knowledgePool += `\n=== ${urlData.text} ===\nURL: ${urlData.url}\nError: Failed to fetch content\n\n`;
            }
        }
        
        await browser.close();
        
        // Save to knowledge_pool.txt
        await fs.writeFile('knowledge_pool.txt', knowledgePool);
        
        res.json({
            message: 'Documentation analyzed and saved to knowledge_pool.txt',
            urls: urlsContent
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

// Modify the app.listen section to initialize Playwright first
app.listen(PORT, async () => {
    await initializePlaywright();
    console.log(`Server is running on port ${PORT}`);
}); 