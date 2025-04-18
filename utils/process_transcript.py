# from download_report import download_report
from download_transcript import download_transcript
from get_transcript_text import get_transcript_text
from utils.get_quarter_and_year import get_quarter_and_year
from utils.get_periodic_from_text import get_periodic_from_text
from utils.extract_date_from_text import extract_date_from_text
from utils.construct_event import construct_event
from utils.upload_to_r2 import upload_to_r2
from utils.construct_path import construct_path
from utils.remove_pdf_extension import remove_pdf_extension

async def process_transcript(page, ticker="AAPL"):
    """
    Orchestrates the entire transcript processing pipeline:
    1. Extracts heading text
    2. Determines periodicity
    3. Extracts dates and fiscal info
    4. Downloads transcript
    5. Constructs paths
    6. Uploads to R2
    7. Returns event object
    
    Args:
        page: Playwright page object
        ticker: Stock ticker symbol
        
    Returns:
        Dictionary containing the constructed event
    """
    try:
        # Step 1: Get and validate heading
        heading = await get_transcript_text(page)
        if not heading:
            print("  [Skipped] No heading found.")
            return None
        
        print(f"Heading found: {heading}")
        
        # Step 2: Determine document characteristics
        periodicity = get_periodic_from_text(heading)
        published_date = extract_date_from_text(heading)
        
        # Step 3: Handle fiscal info
        if periodicity == 'periodic':
            fiscal_year, fiscal_quarter = get_quarter_and_year(heading)
        else:
            fiscal_year = "0000"
            fiscal_quarter = "0"
        
        # Step 4: Download and process file
        transcript_name = await download_transcript(page)
        file_name = remove_pdf_extension(transcript_name)
        
        # Step 5: Construct paths
        path = construct_path(
            ticker=ticker,
            date=published_date,
            file_name=file_name,
            file=transcript_name
        )
        
        # Step 6: Upload to R2
        r2_path = upload_to_r2(f'downloads/{transcript_name}', path)
        
        # Step 7: Construct and return event
        event = construct_event(
            equity_ticker=ticker,
            content_name=file_name,
            content_type="earnings_transcript",
            published_date=published_date,
            r2_url=r2_path,
            periodicity=periodicity,
            fiscal_date=published_date,
            fiscal_year=fiscal_year,
            fiscal_quarter=fiscal_quarter
        )
        
        return event
    
    except Exception as e:
        print(f"Error processing transcript: {str(e)}")
        return None