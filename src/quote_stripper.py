#!/usr/bin/env python3
"""
Smart quote detection and removal for email threads

Removes redundant quoted content while preserving:
1. New content (non-quoted text)
2. Quote headers (first N lines of each quote block for context)
"""

import re
import os
from typing import Tuple, List


class QuoteStripper:
    """Intelligently strip quoted content from emails"""

    # Quote markers (ordered by priority)
    QUOTE_PATTERNS = [
        (r'^>+\s', 'prefix'),           # > quoted lines
        (r'^On .+wrote:', 'header'),    # "On ... wrote:"
        (r'^\d{4}年\d{1,2}月\d{1,2}日.+写道：', 'header'),  # Chinese
        (r'^From:\s', 'forward'),       # Forward markers
        (r'^Sent:\s', 'forward'),
        (r'^-{5,}\s*Original Message\s*-{5,}', 'separator'),
        (r'^_{10,}', 'separator'),
        (r'^={10,}', 'separator'),
    ]

    def __init__(self, keep_quote_lines: int = 10):
        """
        Initialize quote stripper

        Args:
            keep_quote_lines: Number of lines to keep from each quote block
        """
        self.keep_quote_lines = keep_quote_lines
        self.compiled_patterns = [
            (re.compile(pattern, re.MULTILINE), ptype)
            for pattern, ptype in self.QUOTE_PATTERNS
        ]

    def _is_quote_line(self, line: str) -> bool:
        """Check if a line is part of a quote"""
        stripped = line.strip()
        if not stripped:
            return False

        # Check for quote markers
        for pattern, _ in self.compiled_patterns:
            if pattern.match(line):
                return True

        return False

    def _split_content_and_quotes(self, text: str) -> List[Tuple[str, str]]:
        """
        Split text into alternating content and quote blocks

        Returns:
            List of (type, text) tuples where type is 'content' or 'quote'
        """
        lines = text.split('\n')
        blocks = []
        current_block = []
        current_type = None

        for line in lines:
            is_quote = self._is_quote_line(line)
            line_type = 'quote' if is_quote else 'content'

            if current_type is None:
                # First line
                current_type = line_type
                current_block.append(line)
            elif current_type == line_type:
                # Continue current block
                current_block.append(line)
            else:
                # Type changed - save current block and start new one
                if current_block:
                    blocks.append((current_type, '\n'.join(current_block)))
                current_block = [line]
                current_type = line_type

        # Save last block
        if current_block:
            blocks.append((current_type, '\n'.join(current_block)))

        return blocks

    def strip_quotes(self, text: str, max_length: int = 0) -> Tuple[str, dict]:
        """
        Strip redundant quotes from email text

        Args:
            text: Email body text
            max_length: Maximum total length (0 = unlimited)

        Returns:
            Tuple of (stripped_text, metadata)
        """
        if not text:
            return text, {}

        original_length = len(text)
        blocks = self._split_content_and_quotes(text)

        result_parts = []
        quotes_stripped = 0
        quotes_kept_lines = 0

        for block_type, block_text in blocks:
            if block_type == 'content':
                # Keep all content (non-quoted text)
                result_parts.append(block_text)
            else:
                # Quote block - keep only first N lines
                quote_lines = block_text.split('\n')

                if len(quote_lines) <= self.keep_quote_lines:
                    # Small quote block - keep all
                    result_parts.append(block_text)
                    quotes_kept_lines += len(quote_lines)
                else:
                    # Large quote block - keep first N lines + marker
                    kept_lines = quote_lines[:self.keep_quote_lines]
                    result_parts.append('\n'.join(kept_lines))

                    stripped_count = len(quote_lines) - self.keep_quote_lines
                    result_parts.append(f'\n[... {stripped_count} 行引用内容已省略 ...]\n')

                    quotes_stripped += stripped_count
                    quotes_kept_lines += self.keep_quote_lines

        result = '\n'.join(result_parts)

        # Apply hard limit if needed
        hard_truncated = False
        if max_length > 0 and len(result) > max_length:
            result = result[:max_length]
            hard_truncated = True

        metadata = {
            'original_length': original_length,
            'stripped_length': len(result),
            'quote_lines_stripped': quotes_stripped,
            'quote_lines_kept': quotes_kept_lines,
            'hard_truncated': hard_truncated
        }

        return result, metadata


def strip_email_quotes(
    text: str,
    max_length: int = 0,
    keep_quote_lines: int = None
) -> Tuple[str, dict]:
    """
    Convenience function to strip quotes from email text

    Args:
        text: Email body text
        max_length: Maximum total length (0 = unlimited)
        keep_quote_lines: Lines to keep per quote block
                         (None = use MAIL_KEEP_QUOTE_LINES env var, default 10)

    Returns:
        Tuple of (stripped_text, metadata)
    """
    if keep_quote_lines is None:
        keep_quote_lines = int(os.environ.get('MAIL_KEEP_QUOTE_LINES', '10'))

    stripper = QuoteStripper(keep_quote_lines=keep_quote_lines)
    return stripper.strip_quotes(text, max_length)


if __name__ == '__main__':
    # Test example
    test_email = """Hello, I agree with your proposal.

Let me know if you need any changes.

On 2025-01-01, Bob wrote:
> Thanks for the quick response.
>
> I think we should proceed with option A.
> Here are the reasons:
> 1. Better performance
> 2. Lower cost
> 3. Easier maintenance
> 4. More scalable
> 5. Industry standard
> 6. Good documentation
> 7. Active community
> 8. Proven track record
> 9. Compatible with existing systems
> 10. Easy to learn
> 11. More features
> 12. Better support
>
> What do you think?
>
> Best regards,
> Bob
>
>
> On 2024-12-25, Alice wrote:
> > Hi Bob,
> >
> > I wanted to discuss the project timeline.
> > We have two options:
> > Option A: Fast track (2 weeks)
> > Option B: Standard (4 weeks)
> >
> > Let me know your preference.
> >
> > Thanks,
> > Alice"""

    print("Original email:")
    print("=" * 80)
    print(test_email)
    print(f"\nOriginal length: {len(test_email)} chars")

    print("\n" + "=" * 80)
    print("After quote stripping (keep 10 lines):")
    print("=" * 80)

    stripped, metadata = strip_email_quotes(test_email, keep_quote_lines=10)
    print(stripped)

    print("\n" + "=" * 80)
    print("Metadata:")
    print(f"  Original length: {metadata['original_length']} chars")
    print(f"  Stripped length: {metadata['stripped_length']} chars")
    print(f"  Reduction: {(1 - metadata['stripped_length']/metadata['original_length'])*100:.1f}%")
    print(f"  Quote lines kept: {metadata['quote_lines_kept']}")
    print(f"  Quote lines stripped: {metadata['quote_lines_stripped']}")

    print("\n" + "=" * 80)
    print("After quote stripping with hard limit (500 chars):")
    print("=" * 80)

    stripped2, metadata2 = strip_email_quotes(test_email, max_length=500, keep_quote_lines=10)
    print(stripped2)
    print(f"\nFinal length: {len(stripped2)} chars")
    print(f"Hard truncated: {metadata2['hard_truncated']}")
