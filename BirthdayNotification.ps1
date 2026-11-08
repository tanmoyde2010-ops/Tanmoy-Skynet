
# ==========================================
# DAILY BIRTHDAY NOTIFICATION EMAIL SCRIPT
# ==========================================

# CSV file location
$CsvPath = "C:\Birthday\november_famous_birthdays.csv"

# Email configuration
$SenderEmail   = "gff@gmail.com"
$ReceiverEmail = "fgfd@gmail.com"

# Gmail SMTP settings
$SmtpServer = "smtp.gmail.com"
$SmtpPort   = 587

# Hardcoded Gmail App Password
$AppPassword = "abcdefgh"

# Create SMTP credentials without popup
$SecurePassword = ConvertTo-SecureString `
    $AppPassword -AsPlainText -Force

$Credential = New-Object System.Management.Automation.PSCredential(
    $SenderEmail,
    $SecurePassword
)

# SMTP Client
$SMTP = New-Object System.Net.Mail.SmtpClient(
    $SmtpServer,
    $SmtpPort
)

$SMTP.EnableSsl = $true
$SMTP.UseDefaultCredentials = $false
$SMTP.Credentials = $Credential.GetNetworkCredential()
$SMTP.Timeout = 30000

# Get today's date
$Today = (Get-Date).ToString("d MMMM",
    [System.Globalization.CultureInfo]::GetCultureInfo("en-US"))

Write-Host "Checking birthdays for: $Today"

# Read birthday CSV file
if (!(Test-Path $CsvPath)) {
    Write-Host "CSV file not found: $CsvPath" -ForegroundColor Red
    exit
}

$Birthdays = Import-Csv -Path $CsvPath

# Find today's birthdays
$TodaysBirthdays = $Birthdays | Where-Object {
    $_.'Birth Date (November)'.Trim() -eq $Today
}

# Check whether birthdays exist
if ($TodaysBirthdays.Count -eq 0) {
    Write-Host "No birthdays found today."
    exit
}

# Prepare email content
$BirthdayList = ""

foreach ($Person in $TodaysBirthdays) {
    $BirthdayList += @"
    <tr>
        <td style='padding:10px;border:1px solid #ddd;'>
            $($Person.Name)
        </td>
        <td style='padding:10px;border:1px solid #ddd;'>
            $($Person.'Birth Year')
        </td>
    </tr>
"@
}

$Subject = "Birthday Notification - $Today"

$Body = @"
<html>
<body style='font-family:Arial;'>
    <h2 style='color:#4A69BD;'>Birthday Reminder!</h2>

    <p>Hello,</p>

    <p>Here are today's famous birthdays:</p>

    <table style='border-collapse:collapse;width:100%;'>
        <tr style='background-color:#4A69BD;color:white;'>
            <th style='padding:10px;'>Name</th>
            <th style='padding:10px;'>Birth Year</th>
        </tr>
        $BirthdayList
    </table>

    <p>Have a wonderful day!</p>

    <p>Regards,<br>
    Automated Birthday Notification System</p>
</body>
</html>
"@

try {
    # Create email message
    $MailMessage = New-Object System.Net.Mail.MailMessage
    $MailMessage.From = $SenderEmail
    $MailMessage.To.Add($ReceiverEmail)
    $MailMessage.Subject = $Subject
    $MailMessage.Body = $Body
    $MailMessage.IsBodyHtml = $true

    # Configure SMTP client
    $SMTP = New-Object System.Net.Mail.SmtpClient(
        $SmtpServer, $SmtpPort
    )

    $SMTP.EnableSsl = $true
    $SMTP.Credentials = $Credential.GetNetworkCredential()

    # Send email
    $SMTP.Send($MailMessage)

    Write-Host "Birthday notification email sent successfully!" `
        -ForegroundColor Green
}
catch {
    Write-Host "Email sending failed: $($_.Exception.Message)" `
        -ForegroundColor Red
}
finally {
    if ($SMTP) {
        $SMTP.Dispose()
    }

    if ($MailMessage) {
        $MailMessage.Dispose()
    }
}
