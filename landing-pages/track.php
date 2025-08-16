<?php
// track.php - logs email opens with unique ID for phishing simulation

// Security: Disable error display
ini_set('display_errors', 0);
error_reporting(0);

// Get recipient ID from query string
$rid = isset($_GET['id']) ? trim($_GET['id']) : 'unknown';

// Log file path (matches log_parser.py)
$log_file = __DIR__ . '/../logs/email_opens.log';

// Create log entry with timestamp and optional IP
$log_entry = date('Y-m-d H:i:s') . " - Opened by recipient ID: {$rid} - IP: {$_SERVER['REMOTE_ADDR']}\n";

// Append log entry
file_put_contents($log_file, $log_entry, FILE_APPEND | LOCK_EX);

// Output a 1x1 transparent GIF pixel
header('Content-Type: image/gif');
echo base64_decode('R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==');
?>
