from unittest.mock import patch

from rich.text import Text

from regulex import (
    check_regex,
    explain_pattern,
    highlight_matches,
    interactive_mode,
    print_banner,
)


class TestHighlightMatches:
    """Tests for the highlight_matches function."""

    def test_highlight_single_match(self):
        """Test highlighting a single match in text."""
        result = highlight_matches("Hello 123 World", r"\d+")
        assert isinstance(result, Text)
        # Verify the result contains the match
        assert "123" in str(result)

    def test_highlight_multiple_matches(self):
        """Test highlighting multiple matches in text."""
        result = highlight_matches("abc123def456ghi", r"\d+")
        assert isinstance(result, Text)
        text_str = str(result)
        assert "123" in text_str
        assert "456" in text_str

    def test_highlight_no_matches(self):
        """Test highlighting when there are no matches."""
        result = highlight_matches("Hello World", r"\d+")
        assert isinstance(result, Text)
        assert "Hello World" in str(result)

    def test_highlight_entire_text(self):
        """Test highlighting when entire text matches."""
        result = highlight_matches("12345", r"\d+")
        assert isinstance(result, Text)
        assert "12345" in str(result)

    def test_highlight_matches_at_start(self):
        """Test highlighting matches at the beginning of text."""
        result = highlight_matches("123abc", r"\d+")
        assert isinstance(result, Text)
        assert "123" in str(result)

    def test_highlight_matches_at_end(self):
        """Test highlighting matches at the end of text."""
        result = highlight_matches("abc123", r"\d+")
        assert isinstance(result, Text)
        assert "123" in str(result)

    def test_highlight_empty_text(self):
        """Test highlighting with empty text."""
        result = highlight_matches("", r"\d+")
        assert isinstance(result, Text)

    def test_highlight_consecutive_matches(self):
        """Test highlighting consecutive matches."""
        result = highlight_matches("123456", r"\d")
        assert isinstance(result, Text)
        assert "123456" in str(result)


class TestExplainPattern:
    """Tests for the explain_pattern function."""

    def test_explain_digit_pattern(self):
        """Test explanation of digit pattern."""
        result = explain_pattern(r"\d")
        assert "digit" in result.lower()
        assert "0-9" in result

    def test_explain_word_pattern(self):
        """Test explanation of word pattern."""
        result = explain_pattern(r"\w")
        assert "letter" in result.lower() or "alphanumeric" in result.lower()

    def test_explain_whitespace_pattern(self):
        """Test explanation of whitespace pattern."""
        result = explain_pattern(r"\s")
        assert "whitespace" in result.lower()

    def test_explain_dot_pattern(self):
        """Test explanation of dot pattern."""
        result = explain_pattern(r"\.")
        assert "character" in result.lower()

    def test_explain_star_pattern(self):
        """Test explanation of star pattern."""
        result = explain_pattern(r"\*")
        assert "0 or more" in result.lower()

    def test_explain_plus_pattern(self):
        """Test explanation of plus pattern."""
        result = explain_pattern(r"\+")
        assert "1 or more" in result.lower()

    def test_explain_question_pattern(self):
        """Test explanation of question pattern."""
        result = explain_pattern(r"\?")
        assert "0 or 1" in result.lower()

    def test_explain_character_set_pattern(self):
        """Test explanation of character set pattern."""
        result = explain_pattern(r"[abc]")
        assert "character" in result.lower()
        assert "set" in result.lower()

    def test_explain_negated_set_pattern(self):
        """Test explanation of negated character set pattern."""
        result = explain_pattern(r"[^abc]")
        assert "not" in result.lower()

    def test_explain_start_pattern(self):
        """Test explanation of start anchor pattern."""
        result = explain_pattern(r"^")
        assert "start" in result.lower()

    def test_explain_end_pattern(self):
        """Test explanation of end anchor pattern."""
        result = explain_pattern(r"$")
        assert "end" in result.lower()

    def test_explain_non_capturing_group(self):
        """Test explanation of non-capturing group pattern."""
        result = explain_pattern(r"(?:...)")
        assert "non-capturing" in result.lower()

    def test_explain_multiple_patterns(self):
        """Test explanation with multiple patterns in text."""
        result = explain_pattern(r"\d\w\s")
        assert "digit" in result.lower()
        # Should have multiple explanations
        lines = result.split("\n")
        assert len(lines) >= 3

    def test_explain_no_matching_pattern(self):
        """Test explanation when pattern has no known components."""
        result = explain_pattern("xyz123")
        assert "no explanation" in result.lower()

    def test_explain_empty_pattern(self):
        """Test explanation with empty pattern."""
        result = explain_pattern("")
        assert "no explanation" in result.lower()


class TestCheckRegex:
    """Tests for the check_regex function."""

    @patch('regulex.console')
    def test_check_regex_with_matches(self, mock_console):
        """Test regex testing with matches found."""
        check_regex(r"\d+", "abc123def456")
        # Verify that console was called to display results
        assert mock_console.print.called

    @patch('regulex.console')
    def test_check_regex_no_matches(self, mock_console):
        """Test regex testing with no matches."""
        check_regex(r"\d+", "abcdef")
        mock_console.print.assert_called()
        # Check that "No matches" message was displayed
        calls = [str(call) for call in mock_console.print.call_args_list]
        assert any("No matches" in str(call) for call in calls)

    @patch('regulex.console')
    def test_check_regex_invalid_pattern(self, mock_console):
        """Test regex testing with invalid regex pattern."""
        check_regex(r"[invalid", "text")
        # Should catch regex error
        mock_console.print.assert_called()
        calls = [str(call) for call in mock_console.print.call_args_list]
        assert any("error" in str(call).lower() for call in calls)

    @patch('regulex.console')
    def test_check_regex_multiple_matches(self, mock_console):
        """Test regex with multiple matches."""
        check_regex(r"\d", "1a2b3c")
        mock_console.print.assert_called()

    @patch('regulex.console')
    def test_check_regex_single_match(self, mock_console):
        """Test regex with a single match."""
        check_regex(r"\d+", "abc123")
        mock_console.print.assert_called()

    @patch('regulex.console')
    def test_check_regex_empty_text(self, mock_console):
        """Test regex with empty text."""
        check_regex(r"\d+", "")
        mock_console.print.assert_called()

    @patch('regulex.console')
    def test_check_regex_pattern_with_groups(self, mock_console):
        """Test regex with capturing groups."""
        check_regex(r"(\d+)-(\d+)", "123-456")
        mock_console.print.assert_called()


class TestInteractiveMode:
    """Tests for the interactive_mode function."""

    @patch('regulex.console')
    def test_interactive_mode_exit(self, mock_console):
        """Test interactive mode with immediate exit."""
        mock_console.input.side_effect = ["exit"]
        interactive_mode()
        mock_console.input.assert_called()

    @patch('regulex.console')
    def test_interactive_mode_quit(self, mock_console):
        """Test interactive mode with quit command."""
        mock_console.input.side_effect = ["quit"]
        interactive_mode()
        mock_console.input.assert_called()

    @patch('regulex.console')
    def test_interactive_mode_help(self, mock_console):
        """Test interactive mode help command."""
        mock_console.input.side_effect = ["help", "exit"]
        interactive_mode()
        # Verify help panel was printed
        assert mock_console.print.called

    @patch('regulex.console')
    def test_interactive_mode_full_flow(self, mock_console):
        """Test interactive mode with pattern and text input."""
        mock_console.input.side_effect = [r"\d+", "abc123", "exit"]
        interactive_mode()
        # Should have input calls for pattern and text
        assert mock_console.input.call_count >= 2

    @patch('regulex.console')
    def test_interactive_mode_quit_on_text_input(self, mock_console):
        """Test quitting during text input in interactive mode."""
        mock_console.input.side_effect = [r"\d+", "quit"]
        interactive_mode()
        mock_console.input.assert_called()

    @patch('regulex.console')
    def test_interactive_mode_help_then_exit(self, mock_console):
        """Test help followed by exit in interactive mode."""
        mock_console.input.side_effect = ["help", "exit"]
        interactive_mode()
        assert mock_console.print.called


class TestPrintBanner:
    """Tests for the print_banner function."""

    @patch('builtins.print')
    def test_print_banner_output(self, mock_print):
        """Test that banner is printed."""
        print_banner()
        mock_print.assert_called()
        call_args = mock_print.call_args[0][0]
        assert "r e g u l e x" in call_args

    @patch('builtins.print')
    def test_print_banner_contains_box(self, mock_print):
        """Test that banner contains box drawing characters."""
        print_banner()
        call_args = mock_print.call_args[0][0]
        assert "╔" in call_args or "║" in call_args or "╚" in call_args

    @patch('builtins.print')
    def test_print_banner_contains_title(self, mock_print):
        """Test that banner contains the title."""
        print_banner()
        call_args = mock_print.call_args[0][0]
        assert "r e g u l e x" in call_args


class TestRegexPatterns:
    """Integration tests with real regex patterns."""

    def test_digit_pattern(self):
        """Test basic digit pattern."""
        result = highlight_matches("abc123def", r"\d+")
        assert isinstance(result, Text)

    def test_email_pattern(self):
        """Test email-like pattern."""
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        result = highlight_matches("test@example.com", email_pattern)
        assert isinstance(result, Text)

    def test_date_pattern(self):
        """Test date pattern DD-MM-YYYY."""
        date_pattern = r"\d{2}-\d{2}-\d{4}"
        result = highlight_matches("Today is 25-12-2023", date_pattern)
        assert isinstance(result, Text)

    def test_word_boundary_pattern(self):
        """Test word boundary pattern."""
        pattern = r"\b\w{4}\b"
        result = highlight_matches("This is a test case", pattern)
        assert isinstance(result, Text)

    def test_case_insensitive_pattern(self):
        """Test case-insensitive pattern."""
        pattern = r"(?i)hello"
        result = highlight_matches("HELLO hello Hello", pattern)
        assert isinstance(result, Text)

    def test_alternation_pattern(self):
        """Test alternation pattern."""
        pattern = r"cat|dog|bird"
        result = highlight_matches("I have a cat and a dog", pattern)
        assert isinstance(result, Text)

    def test_optional_pattern(self):
        """Test optional pattern."""
        pattern = r"colou?r"
        result = highlight_matches("color colour", pattern)
        assert isinstance(result, Text)

    def test_quantifier_pattern(self):
        """Test quantifier pattern."""
        pattern = r"\d{3}-\d{3}-\d{4}"
        result = highlight_matches("123-456-7890", pattern)
        assert isinstance(result, Text)

    def test_character_class_pattern(self):
        """Test character class pattern."""
        pattern = r"[aeiou]"
        result = highlight_matches("Hello World", pattern)
        assert isinstance(result, Text)

    def test_negated_character_class_pattern(self):
        """Test negated character class pattern."""
        pattern = r"[^aeiou]"
        result = highlight_matches("Hello", pattern)
        assert isinstance(result, Text)


class TestEdgeCases:
    """Tests for edge cases and special scenarios."""

    def test_special_characters_in_text(self):
        """Test with special characters in text."""
        result = highlight_matches("Price: $99.99", r"\$\d+\.\d+")
        assert isinstance(result, Text)

    def test_unicode_text(self):
        """Test with unicode characters."""
        result = highlight_matches("Hello 世界 123", r"\d+")
        assert isinstance(result, Text)

    def test_newline_in_text(self):
        """Test with newline characters."""
        text = "Line1\nLine2\nLine3"
        result = highlight_matches(text, r"Line\d")
        assert isinstance(result, Text)

    def test_very_long_text(self):
        """Test with very long text."""
        long_text = "abc123" * 1000
        result = highlight_matches(long_text, r"\d+")
        assert isinstance(result, Text)

    def test_very_long_pattern(self):
        """Test with very complex pattern."""
        pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        result = highlight_matches("contact@example.co.uk", pattern)
        assert isinstance(result, Text)

    def test_escaped_special_regex_chars(self):
        """Test with escaped special regex characters."""
        result = highlight_matches("Price: 100*2", r"\d+\*\d+")
        assert isinstance(result, Text)

    def test_parentheses_in_pattern(self):
        """Test pattern with parentheses."""
        result = highlight_matches("Phone: (123) 456-7890", r"\(\d{3}\)")
        assert isinstance(result, Text)

    def test_backslash_in_text(self):
        """Test with backslash in text."""
        result = highlight_matches("C:\\Users\\test", r"\\")
        assert isinstance(result, Text)

    def test_empty_pattern_match(self):
        """Test with pattern that matches empty strings."""
        result = highlight_matches("abc", r"a*")
        assert isinstance(result, Text)


class TestPatternExplanations:
    """Tests for comprehensive pattern explanations."""

    def test_quantifier_explanations(self):
        """Test explanations for quantifiers."""
        patterns = [r"\*", r"\+", r"\?", r"{n}", r"{n,m}"]
        for pattern in patterns:
            result = explain_pattern(pattern)
            assert isinstance(result, str)
            assert len(result) > 0

    def test_anchor_explanations(self):
        """Test explanations for anchors."""
        patterns = [r"^", r"$"]
        for pattern in patterns:
            result = explain_pattern(pattern)
            assert isinstance(result, str)
            assert len(result) > 0

    def test_character_class_explanations(self):
        """Test explanations for character classes."""
        patterns = [r"[abc]", r"[^abc]"]
        for pattern in patterns:
            result = explain_pattern(pattern)
            assert isinstance(result, str)
            assert len(result) > 0

    def test_escape_sequence_explanations(self):
        """Test explanations for escape sequences."""
        patterns = [r"\d", r"\w", r"\s"]
        for pattern in patterns:
            result = explain_pattern(pattern)
            assert isinstance(result, str)
            assert len(result) > 0


class TestRealWorldPatterns:
    """Tests with real-world regex patterns."""

    def test_ipv4_address_pattern(self):
        """Test IPv4 address pattern."""
        pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
        result = highlight_matches("Server: 192.168.1.1", pattern)
        assert isinstance(result, Text)

    def test_url_pattern(self):
        """Test URL pattern."""
        pattern = r"https?://[^\s]+"
        result = highlight_matches("Visit https://example.com for more", pattern)
        assert isinstance(result, Text)

    def test_phone_number_pattern(self):
        """Test phone number pattern."""
        pattern = r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"
        result = highlight_matches("Call 123-456-7890", pattern)
        assert isinstance(result, Text)

    def test_credit_card_pattern(self):
        """Test credit card pattern."""
        pattern = r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b"
        result = highlight_matches("Card: 1234 5678 9012 3456", pattern)
        assert isinstance(result, Text)

    def test_ipv6_address_pattern(self):
        """Test IPv6 address pattern (simplified)."""
        pattern = r"[0-9a-fA-F]{1,4}:[0-9a-fA-F]{1,4}"
        result = highlight_matches("IPv6: 2001:0db8", pattern)
        assert isinstance(result, Text)

    def test_html_tag_pattern(self):
        """Test HTML tag pattern."""
        pattern = r"<[^>]+>"
        result = highlight_matches("<div class='test'>content</div>", pattern)
        assert isinstance(result, Text)

    def test_markdown_link_pattern(self):
        """Test markdown link pattern."""
        pattern = r"\[([^\]]+)\]\(([^)]+)\)"
        result = highlight_matches("[GitHub](https://github.com)", pattern)
        assert isinstance(result, Text)
