#!/bin/bash
# Mail Message-ID Copy Quick Action
# Copy the first Message-ID from selected emails in Mail.app
# Optimized: Direct AppleScript property access - instant even with large attachments

osascript <<'EOF'
tell application "Mail"
    set selectedMessages to selection

    if (count of selectedMessages) is 0 then
        display notification "Please select an email first" with title "Copy Message-ID"
        do shell script "afplay /System/Library/Sounds/Basso.aiff"
        return
    end if

    -- Get the first message's Message-ID directly
    -- This uses Apple's built-in property, no need to parse email source
    repeat with msg in (get selectedMessages)
        try
            set msgID to message id of msg

            if msgID is not "" then
                -- Ensure Message-ID is wrapped in angle brackets (RFC 5322 standard)
                if msgID does not start with "<" then
                    set msgID to "<" & msgID & ">"
                end if

                -- Found Message-ID, copy and exit
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
