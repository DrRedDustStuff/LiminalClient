## TODO - Escape The Backrooms Modloader (Inspired by Modrinth)

1. Project Setup
    - Done.  Initialize repository and folder structure
    - Set up basic README and documentation **(meh)**

2. Core Features
    - Mod listing: Display available mods with details (name, author, version, description)
    - Mod download & install: Allow users to download and install mods
    - Mod update: Check for and apply updates to installed mods
    - Mod removal: Uninstall mods cleanly

3. User Interface
    - Design main UI similar to Modrinth (modern, clean, intuitive)
    - - Modpack-Page
    - - Settings-Page
    - - Home-Page
    - Implement mod search and filter functionality
    - Add mod detail pages with screenshots, changelogs, and download stats -close to done

4. Mod Management
    - Support for mod dependencies and compatibility checks
    - Enable mod enable/disable toggling
    - Show installed mods and their status

5. Backend Integration
    *Note: finished backend mod file type.
    - Connect to a mod database or API (self-hosted or third-party)
    - - finish mod database/mod file requesting
    - Implement mod upload and moderation tools (for creators)
    - - finish mod file upload requesting

6. Security & Validation
    - Validate mod files before installation -optional
    - Sandbox mod execution to prevent malicious behavior -optional -probably hard

7. Community Features
    - User accounts and authentication
    - Ratings, reviews, and comments for mods -low priority

8. Testing & QA
    - Unit and integration tests for core features
    - Beta release and feedback collection

9. Documentation & Release
    - Write user and developer guides
    - Prepare for public release

10. Future Enhancements
    - Support for modpacks
    - Automatic conflict resolution -optional
    - Localization/multi-language support -optional #system rewrite

- Redo translation manager and translatables -done
- Rename variables to make sense with the api they use -in progress