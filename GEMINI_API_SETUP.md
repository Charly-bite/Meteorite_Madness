# Gemini AI API Setup Guide

## Getting Your API Key

1. **Visit Google AI Studio**
   - Go to [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account

2. **Create API Key**
   - Click "Create API Key"
   - Select a Google Cloud project or create a new one
   - Copy the generated API key

3. **Configure the Application**
   - Open `/home/byte/Meteorite Madness/templates/impact_simulation.html`
   - Find the line: `const GEMINI_API_KEY = 'YOUR_GEMINI_API_KEY';`
   - Replace `YOUR_GEMINI_API_KEY` with your actual API key

## Features Enabled by AI Integration

### 🛡️ Defense Strategy Generator
- Click "AI Defense Strategy" button
- Generates comprehensive planetary defense plans including:
  - Detection requirements
  - Deflection methods (kinetic impactor, nuclear, gravity tractor)
  - Mission timeline and requirements
  - Backup plans
  - Evacuation protocols

### 📝 Impact Narrative Report
- Click "AI Impact Report" button
- Generates detailed impact assessment including:
  - Immediate impact effects (blast, thermal, seismic)
  - Environmental consequences
  - Casualty estimates
  - Infrastructure damage
  - Long-term recovery timeline

## API Usage Notes

- **Free Tier**: Gemini API offers a generous free tier
- **Rate Limits**: Be mindful of API rate limits
- **Model**: Currently using `gemini-2.0-flash-exp` (fast and efficient)
- **Cost**: Check current pricing at [Google AI Pricing](https://ai.google.dev/pricing)

## Security Best Practices

⚠️ **Important**: Never commit API keys to version control!

For production deployment, consider:
1. Using environment variables
2. Backend API proxy to hide the key
3. Implementing API key rotation
4. Monitoring API usage

## Alternative: Environment Variable Setup

For better security, you can modify the code to use environment variables:

```javascript
const GEMINI_API_KEY = '{{ gemini_api_key }}'; // Flask template variable
```

Then in your Flask app:
```python
import os

@app.route('/impact-simulation')
def impact_simulation():
    return render_template('impact_simulation.html', 
                         gemini_api_key=os.environ.get('GEMINI_API_KEY'))
```

Set the environment variable:
```bash
export GEMINI_API_KEY="your-actual-api-key-here"
```

## Troubleshooting

**Error: "AI generation failed"**
- Check your API key is correct
- Verify internet connection
- Check browser console for detailed error messages
- Ensure you haven't exceeded API rate limits

**Empty Response**
- Check API key permissions
- Verify the model name is correct
- Review API quota in Google Cloud Console

## Testing

1. Set up your API key
2. Navigate to http://localhost:5000/impact-simulation
3. Adjust meteorite parameters
4. Click "Run Simulation"
5. Click "AI Defense Strategy" to test AI generation
6. Click "AI Impact Report" to test narrative generation

The AI output will appear in the blue-bordered box below the buttons.
