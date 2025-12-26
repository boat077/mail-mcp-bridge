#!/bin/bash
# Mail Message-ID Copy Quick Action
# Copy the first Message-ID from selected emails in Mail.app
# Optimized: Only processes first 5000 chars for performance

osascript <<'EOF'
tell application "Mail"
    set selectedMessages to selection

    if (count of selectedMessages) is 0 then
        display notification "Please select an email first" with title "Copy Message-ID"
        do shell script "afplay /System/Library/Sounds/Basso.aiff"
        return
    end if

    -- Only get the first successful Message-ID
    -- (One ID is enough for read_thread to get entire conversation)
    repeat with msg in selectedMessages
        try
            -- Get email source
            set msgSource to source of msg

            -- Only take first 5000 characters (email headers won't exceed this)
            -- Performance optimization: Large attachment emails (3.6MB) process in <1 second
            set msgHeader to ""
            try
                set sourceLen to length of msgSource
                if sourceLen > 5000 then
                    set msgHeader to text 1 thru 5000 of msgSource
                else
                    set msgHeader to msgSource
                end if
            on error
                set msgHeader to msgSource
            end try

            -- Extract Message-ID (case-insensitive)
            -- Supports both "Message-ID" and "Message-Id" formats
            set msgID to do shell script "echo " & quoted form of msgHeader & " | awk '/^[Mm]essage-[Ii][dD]:/ {gsub(/^[Mm]essage-[Ii][dD]: */, \"\"); print; exit}' | tr -d '\\r\\n' | xargs"

            if msgID is not "" then
                -- Found first valid Message-ID, copy and exit
                set the clipboard to msgID
                display notification msgID with title "✅ Message-ID Copied"
                do shell script "afplay /System/Library/Sounds/Glass.aiff"
                return
            end if

        on error errMsg
            -- Continue to next email if current one fails
        end try
    end repeat

    -- If all emails failed
    display notification "Could not extract Message-ID from selected emails" with title "❌ Extraction Failed"
    do shell script "afplay /System/Library/Sounds/Basso.aiff"
end tell
EOF
