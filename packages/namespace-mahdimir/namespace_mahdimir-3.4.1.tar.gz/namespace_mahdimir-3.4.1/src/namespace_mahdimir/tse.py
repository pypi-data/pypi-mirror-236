class Col :
    jd = "JDate"
    jm = "JMonth"
    jyr = "JYear"
    tse_id = "TSETMC-ID"
    tic = "Ticker"
    btic = "BaseTicker"
    ftic = "FirmTicker"
    eng_ftic = "EngFirmTicker"
    name = "Name"
    d = "Date"
    dt = "DateTime"
    ahi = "AdjHigh"
    alow = "AdjLow"
    aopen = "AdjOpen"
    aclose = "AdjClose"
    aclose_lin = 'AdjClose-LinearlyFilled'
    vol = "Volume"
    alast = "AdjLast"
    is_tse_open = "Is-TSE-Open"
    wd = "WeekDay"
    arlo = "AdjRet-SinceLastOpenDay"
    ar1d = "AdjRet-1WorkDay"
    ar1dlf = "AdjRet-1WorkDay-LinearFilled"
    is_tic_open = "IsTickerOpen"
    ind_id = "IndexID"
    obsd = "ObsDate"
    close = "Close"
    tedpix_close = "TEDPIX-Close"
    rf_apr = "RiskFree-Rate-APR"
    rf_d = "RiskFree-Rate-Daily"
    tedpix_ret = "TEDPIX-Return"
    tedpix_exss_ret = "TEDPIX-Excess-Return"
    exss_ret = "Excess-Return"
    get_date = 'GetDate'
    val = 'Value'
    trd_count = 'TradeCount'
    mktcap = 'MarketCap'

class CodalCol :
    TracingNo = "TracingNo"
    SuperVision = "SuperVision"
    Symbol = "Symbol"
    CompanyName = "CompanyName"
    UnderSupervision = "UnderSupervision"
    Title = "Title"
    LetterCode = "LetterCode"
    SentDateTime = "SentDateTime"
    PublishDateTime = "PublishDateTime"
    HasHtml = "HasHtml"
    Url = "Url"
    HasExcel = "HasExcel"
    HasPdf = "HasPdf"
    HasXbrl = "HasXbrl"
    HasAttachment = "HasAttachment"
    AttachmentUrl = "AttachmentUrl"
    PdfUrl = "PdfUrl"
    ExcelUrl = "ExcelUrl"
    XbrlUrl = "XbrlUrl"
    TedanUrl = "TedanUrl"

class DAllCodalLetters :
    TracingNo = "TracingNo"
    CodalTicker = "CodalTicker"
    CompanyName = "CompanyName"
    LetterCode = "LetterCode"
    Title = "Title"
    SentDateTime = "SentDateTime"
    PublishDateTime = "PublishDateTime"
    UnderSupervision = "UnderSupervision"
    SuperVision_UnderSupervision = "SuperVision.UnderSupervision"
    SuperVision_AdditionalInfo = "SuperVision.AdditionalInfo"
    SuperVision_Reasons = "SuperVision.Reasons"
    IsEstimate = "IsEstimate"
    TedanUrl = "TedanUrl"
    HasHtml = "HasHtml"
    Url = "Url"
    HasAttachment = "HasAttachment"
    AttachmentUrl = "AttachmentUrl"
    HasExcel = "HasExcel"
    ExcelUrl = "ExcelUrl"
    HasPdf = "HasPdf"
    PdfUrl = "PdfUrl"
    HasXbrl = "HasXbrl"
    XbrlUrl = "XbrlUrl"

class CodalLetterCode :
    MonthlySalesRep = "ن-۳۰"

class CodalMonthlySalesFirmType :
    p = "Production"
    s = "Service"
    b = "Bank"
    i = "Insurance"
    l = "Leasing"
    r = "RealEstate"
    a = "Agriculture"
    f = "Financing"

class DIndInsCols :
    bdc = 'Buy-Ind-Count'
    bsc = 'Buy-Ins-Count'
    sdc = 'Sell-Ind-Count'
    ssc = 'Sell-Ins-Count'

    bdv = 'Buy-Ind-Vol'
    bsv = 'Buy-Ins-Vol'
    sdv = 'Sell-Ind-Vol'
    ssv = 'Sell-Ins-Vol'

    bdva = 'Buy-Ind-Val'
    bsva = 'Buy-Ins-Val'
    sdva = 'Sell-Ind-Val'
    ssva = 'Sell-Ins-Val'

class DNomPriceCol :
    _c = Col()

    # cols from Col
    ftic = _c.ftic
    tse_id = _c.tse_id
    d = _c.d
    jd = _c.jd

    # order as tsetmc.com
    nhi = 'NomHigh'
    nlo = 'NomLow'
    nclos = 'NomClose'
    nlst = 'NomLast'
    nopn = 'NomOpen'
    nystrd = 'NomYesterdayClose'
    val = 'Value'
    vol = 'Volume'
    trd_count = 'TradeCount'

class D0OutstandingSharesCol :
    _c = Col()

    # cols from Col
    ftic = _c.ftic
    tse_id = _c.tse_id
    d = _c.d
    jd = _c.jd

    # others
    os = 'OutstandingShares'

class DOutstandingSharesCol :
    _c = Col()
    _cd = D0OutstandingSharesCol()

    # cols from Col
    ftic = _c.ftic
    d = _c.d
    jd = _c.jd

    os = _cd.os

class DMarketCap :
    _c = Col()

    # cols from Col
    ftic = _c.ftic
    d = _c.d
    jd = _c.jd
    mkcap = _c.mktcap
