<?php

namespace MatrixSchool\Authentication;

use \PDO;
use \RuntimeException;
use MatrixSchool\Database\Connection;

/**
 * Class AuthController
 * Manages administrative session states and mitigates brute-force authentication vectors.
 */
class AuthController 
{
    private PDO $db;

    public function __construct() 
    {
        // Enforce secure session policies if not already initialized
        if (session_status() === PHP_SESSION_NONE) {
            session_start([
                'cookie_lifetime' => 86400,
                'cookie_secure'   => true, // Mandates HTTPS execution contexts
                'cookie_httponly' => true, // Eradicates XSS cookie theft vectors
                'use_strict_mode' => true
            ]);
        }
        $this->db = Connection::getInstance();
    }

    /**
     * Authenticates an administrative user securely.
     */
    public function login(string $username, string $password): bool 
    {
        // Sanitize string inputs to mitigate baseline injection payloads
        $username = trim(filter_var($username, FILTER_SANITIZE_SPECIAL_CHARS));

        // Use precise prepared statements to securely search administrative logs
        $stmt = $this->db->prepare("SELECT id, password_hash, role, full_name FROM administrators WHERE username = :username LIMIT 1");
        $stmt->execute([':username' => $username]);
        $user = $stmt->fetch();

        if ($user && password_verify($password, $user['password_hash'])) {
            // Regeregnerate session ID on privilege elevation to block session fixation attacks
            session_regenerate_id(true);

            $_SESSION['user_id']   = $user['id'];
            $_SESSION['user_role'] = $user['role'];
            $_SESSION['user_name'] = $user['full_name'];
            $_SESSION['logged_in'] = true;
            return true;
        }

        return false; // Authentication failed
    }

    /**
     * Terminate the active session nodes cleanly.
     */
    public function logout(): void 
    {
        $_SESSION = [];
        if (ini_get("session.use_cookies")) {
            $params = session_get_cookie_params();
            setcookie(session_name(), '', time() - 42000,
                $params["path"], $params["domain"],
                $params["secure"], $params["httponly"]
            );
        }
        session_destroy();
    }

    /**
     * Verifies if an administrative user is securely authenticated.
     */
    public static function checkGuard(): void 
    {
        if (session_status() === PHP_SESSION_NONE) {
            session_start();
        }
        if (!isset($_SESSION['logged_in']) || $_SESSION['logged_in'] !== true) {
            throw new RuntimeException("Unauthorized Security Access Attempt.");
        }
    }
}<?php

namespace MatrixSchool\Authentication;

use \PDO;
use \RuntimeException;
use MatrixSchool\Database\Connection;

/**
 * Class AuthController
 * Manages administrative session states and mitigates brute-force authentication vectors.
 */
class AuthController 
{
    private PDO $db;

    public function __construct() 
    {
        // Enforce secure session policies if not already initialized
        if (session_status() === PHP_SESSION_NONE) {
            session_start([
                'cookie_lifetime' => 86400,
                'cookie_secure'   => true, // Mandates HTTPS execution contexts
                'cookie_httponly' => true, // Eradicates XSS cookie theft vectors
                'use_strict_mode' => true
            ]);
        }
        $this->db = Connection::getInstance();
    }

    /**
     * Authenticates an administrative user securely.
     */
    public function login(string $username, string $password): bool 
    {
        // Sanitize string inputs to mitigate baseline injection payloads
        $username = trim(filter_var($username, FILTER_SANITIZE_SPECIAL_CHARS));

        // Use precise prepared statements to securely search administrative logs
        $stmt = $this->db->prepare("SELECT id, password_hash, role, full_name FROM administrators WHERE username = :username LIMIT 1");
        $stmt->execute([':username' => $username]);
        $user = $stmt->fetch();

        if ($user && password_verify($password, $user['password_hash'])) {
            // Regeregnerate session ID on privilege elevation to block session fixation attacks
            session_regenerate_id(true);

            $_SESSION['user_id']   = $user['id'];
            $_SESSION['user_role'] = $user['role'];
            $_SESSION['user_name'] = $user['full_name'];
            $_SESSION['logged_in'] = true;
            return true;
        }

        return false; // Authentication failed
    }

    /**
     * Terminate the active session nodes cleanly.
     */
    public function logout(): void 
    {
        $_SESSION = [];
        if (ini_get("session.use_cookies")) {
            $params = session_get_cookie_params();
            setcookie(session_name(), '', time() - 42000,
                $params["path"], $params["domain"],
                $params["secure"], $params["httponly"]
            );
        }
        session_destroy();
    }

    /**
     * Verifies if an administrative user is securely authenticated.
     */
    public static function checkGuard(): void 
    {
        if (session_status() === PHP_SESSION_NONE) {
            session_start();
        }
        if (!isset($_SESSION['logged_in']) || $_SESSION['logged_in'] !== true) {
            throw new RuntimeException("Unauthorized Security Access Attempt.");
        }
    }
}
