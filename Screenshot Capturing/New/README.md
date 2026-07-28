# Screenshot Tool V1

A Java Swing application for capturing screenshots and saving them to a Word document.

## Version 1.0 Features

- **Take Screenshot**: Captures the full screen (window minimizes temporarily)
- **Add Comment**: Adds text comments to the last screenshot or as standalone entries
- **Stop & Save**: Saves all captured screenshots to a Word document (.docx) at the selected location
- **Browse**: Select custom save location for the Word document
- **Step Numbers**: Optional checkbox to add step numbers to each entry

## V1 Improvements

- **Visible Buttons**: Standard 3D raised/lowered bevel buttons with hover effects
- **Fixed File Saving**: Properly saves to the specified path with validation
- **Compact Size**: 3x3 inch window (288x288 pixels) - resizable
- **Keyboard Shortcuts**: Ctrl+T (screenshot), Ctrl+S (save)

## Requirements

- Java 8 or higher (tested with Java 21)

## How to Run

Double-click the `ScreenshotToolV1.jar` file, or run from command line:

```bash
java -jar ScreenshotToolV1.jar
```

## Usage Instructions

1. **Set Save Location**: Click "Browse..." to select where to save the Word document
2. **Capture Screenshots**: 
   - Click "Take Screenshot" to capture the full screen
   - The window will minimize briefly during capture
3. **Add Comments**: 
   - Type a comment in the text area
   - Click "Add Comment" to attach it to the last screenshot
4. **Step Numbers**: Check/uncheck "Add Step Numbers" to include step numbers in the document
5. **Save Document**: Click "Stop & Save" to generate the Word document with all screenshots
6. **Clear All**: Click to start a fresh session without saving

## Output

The tool generates a Word document (.docx) containing:
- Title: "Screenshot Documentation"
- Timestamp of generation
- Each screenshot with optional step number and comment
- Screenshots are automatically scaled to fit page width

## Build from Source

Run `build.bat` to compile and package the JAR with all dependencies.

## Dependencies

- Apache POI 5.2.5 (for Word document generation)
- Commons Collections 4.4
- Commons Compress 1.25.0
- Commons IO 2.15.1
- XMLBeans 5.2.0
- Log4j API 2.22.1

All dependencies are bundled in the fat JAR.
