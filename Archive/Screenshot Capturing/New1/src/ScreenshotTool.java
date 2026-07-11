import javax.swing.*;
import javax.swing.border.*;
import javax.swing.filechooser.FileNameExtensionFilter;
import java.awt.*;
import java.awt.event.*;
import java.awt.image.BufferedImage;
import java.io.*;
import java.util.ArrayList;
import java.util.List;
import org.apache.poi.xwpf.usermodel.*;
import org.apache.poi.util.Units;
import javax.imageio.ImageIO;

/**
 * ScreenshotTool - A utility for capturing screenshots and saving them to a Word document
 * Designed by SSI Testing
 * 
 * Features:
 * - Take Screenshot: Captures full screen
 * - Add Comment: Adds text comment with the screenshot
 * - Stop & Save: Saves all screenshots to Word document at specified location
 * - Browse: Select save path
 * - Step Number checkbox: Adds step numbers if checked
 */
public class ScreenshotTool extends JFrame {
    
    private static final String DESIGNED_BY = "Designed by SSI Testing";
    
    private JTextField pathField;
    private JTextArea commentArea;
    private JCheckBox stepNumberCheckbox;
    private JLabel statusLabel;
    private JLabel countLabel;
    
    private List<ScreenshotEntry> screenshots;
    private int stepNumber;
    private String savePath;
    
    // Inner class to hold screenshot data
    private static class ScreenshotEntry {
        BufferedImage image;
        String comment;
        int stepNum;
        
        ScreenshotEntry(BufferedImage image, String comment, int stepNum) {
            this.image = image;
            this.comment = comment;
            this.stepNum = stepNum;
        }
    }
    
    public ScreenshotTool() {
        super("Screenshot Tool - " + DESIGNED_BY);
        screenshots = new ArrayList<>();
        stepNumber = 0;
        savePath = System.getProperty("user.home") + File.separator + "Screenshots.docx";
        
        initializeUI();
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        
        // Set window size to 3x3 inches (at 96 DPI: 288x288 pixels)
        setSize(320, 350);
        setMinimumSize(new Dimension(280, 300));
        setLocationRelativeTo(null);
        setResizable(true);
    }
    
    private void initializeUI() {
        // Main panel with compact padding
        JPanel mainPanel = new JPanel(new BorderLayout(5, 5));
        mainPanel.setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));
        
        // Top panel - Path selection (compact)
        JPanel pathPanel = new JPanel(new BorderLayout(3, 0));
        pathPanel.setBorder(BorderFactory.createTitledBorder(
            BorderFactory.createEtchedBorder(), "Save Location", 
            TitledBorder.LEFT, TitledBorder.TOP, 
            new Font("SansSerif", Font.PLAIN, 10)));
        
        pathField = new JTextField(savePath);
        pathField.setEditable(false);
        pathField.setFont(new Font("SansSerif", Font.PLAIN, 9));
        pathField.setToolTipText(savePath);
        
        JButton browseButton = createStyledButton("...", new Color(180, 180, 180), Color.BLACK);
        browseButton.setPreferredSize(new Dimension(30, 22));
        browseButton.setToolTipText("Browse for save location");
        browseButton.addActionListener(e -> selectSavePath());
        
        pathPanel.add(pathField, BorderLayout.CENTER);
        pathPanel.add(browseButton, BorderLayout.EAST);
        
        // Center panel - Comment area and checkbox (compact)
        JPanel centerPanel = new JPanel(new BorderLayout(3, 3));
        centerPanel.setBorder(BorderFactory.createTitledBorder(
            BorderFactory.createEtchedBorder(), "Comment", 
            TitledBorder.LEFT, TitledBorder.TOP,
            new Font("SansSerif", Font.PLAIN, 10)));
        
        commentArea = new JTextArea(2, 20);
        commentArea.setLineWrap(true);
        commentArea.setWrapStyleWord(true);
        commentArea.setFont(new Font("SansSerif", Font.PLAIN, 10));
        JScrollPane scrollPane = new JScrollPane(commentArea);
        scrollPane.setPreferredSize(new Dimension(200, 40));
        
        stepNumberCheckbox = new JCheckBox("Add Step #", true);
        stepNumberCheckbox.setFont(new Font("SansSerif", Font.PLAIN, 10));
        
        centerPanel.add(scrollPane, BorderLayout.CENTER);
        centerPanel.add(stepNumberCheckbox, BorderLayout.SOUTH);
        
        // Button panel - Standard visible buttons
        JPanel buttonPanel = new JPanel(new GridLayout(2, 2, 5, 5));
        buttonPanel.setBorder(BorderFactory.createEmptyBorder(5, 0, 5, 0));
        
        JButton takeScreenshotBtn = createStyledButton("Take Screenshot", new Color(200, 230, 200), Color.BLACK);
        takeScreenshotBtn.setToolTipText("Capture full screen (Ctrl+T)");
        takeScreenshotBtn.addActionListener(e -> takeScreenshot());
        
        JButton addCommentBtn = createStyledButton("Add Comment", new Color(200, 220, 240), Color.BLACK);
        addCommentBtn.setToolTipText("Add comment to last screenshot");
        addCommentBtn.addActionListener(e -> addComment());
        
        JButton stopBtn = createStyledButton("Stop & Save", new Color(240, 200, 200), Color.BLACK);
        stopBtn.setToolTipText("Save document and exit");
        stopBtn.addActionListener(e -> stopAndSave());
        
        JButton clearBtn = createStyledButton("Clear All", new Color(220, 220, 220), Color.BLACK);
        clearBtn.setToolTipText("Clear all screenshots");
        clearBtn.addActionListener(e -> clearAll());
        
        buttonPanel.add(takeScreenshotBtn);
        buttonPanel.add(addCommentBtn);
        buttonPanel.add(stopBtn);
        buttonPanel.add(clearBtn);
        
        // Status panel (compact)
        JPanel statusPanel = new JPanel(new BorderLayout());
        statusPanel.setBorder(BorderFactory.createEmptyBorder(3, 0, 0, 0));
        statusLabel = new JLabel("Ready");
        statusLabel.setFont(new Font("SansSerif", Font.PLAIN, 9));
        countLabel = new JLabel("Count: 0");
        countLabel.setFont(new Font("SansSerif", Font.BOLD, 9));
        statusPanel.add(statusLabel, BorderLayout.WEST);
        statusPanel.add(countLabel, BorderLayout.EAST);
        
        // Branding panel - "Designed by SSI Testing"
        JPanel brandingPanel = new JPanel(new FlowLayout(FlowLayout.CENTER));
        JLabel brandingLabel = new JLabel(DESIGNED_BY);
        brandingLabel.setFont(new Font("SansSerif", Font.ITALIC, 9));
        brandingLabel.setForeground(new Color(100, 100, 100));
        brandingPanel.add(brandingLabel);
        
        // Bottom container with status and branding
        JPanel bottomContainer = new JPanel(new BorderLayout());
        bottomContainer.add(statusPanel, BorderLayout.NORTH);
        bottomContainer.add(brandingPanel, BorderLayout.SOUTH);
        
        // Assemble main panel
        JPanel topContainer = new JPanel(new BorderLayout(0, 5));
        topContainer.add(pathPanel, BorderLayout.NORTH);
        topContainer.add(centerPanel, BorderLayout.CENTER);
        
        mainPanel.add(topContainer, BorderLayout.NORTH);
        mainPanel.add(buttonPanel, BorderLayout.CENTER);
        mainPanel.add(bottomContainer, BorderLayout.SOUTH);
        
        add(mainPanel);
        
        // Add keyboard shortcuts
        setupKeyboardShortcuts();
    }
    
    /**
     * Creates a styled button with visible borders and proper appearance
     */
    private JButton createStyledButton(String text, Color bgColor, Color fgColor) {
        JButton button = new JButton(text);
        button.setFont(new Font("SansSerif", Font.BOLD, 10));
        button.setBackground(bgColor);
        button.setForeground(fgColor);
        button.setFocusPainted(false);
        button.setOpaque(true);
        button.setBorderPainted(true);
        
        // Create a compound border: raised bevel + padding
        Border raisedBorder = BorderFactory.createRaisedBevelBorder();
        Border paddingBorder = BorderFactory.createEmptyBorder(5, 10, 5, 10);
        button.setBorder(BorderFactory.createCompoundBorder(raisedBorder, paddingBorder));
        
        // Add hover effect
        button.addMouseListener(new MouseAdapter() {
            Color originalBg = bgColor;
            
            @Override
            public void mouseEntered(MouseEvent e) {
                button.setBackground(originalBg.brighter());
                button.setBorder(BorderFactory.createCompoundBorder(
                    BorderFactory.createRaisedBevelBorder(),
                    BorderFactory.createEmptyBorder(5, 10, 5, 10)));
            }
            
            @Override
            public void mouseExited(MouseEvent e) {
                button.setBackground(originalBg);
                button.setBorder(BorderFactory.createCompoundBorder(
                    BorderFactory.createRaisedBevelBorder(),
                    BorderFactory.createEmptyBorder(5, 10, 5, 10)));
            }
            
            @Override
            public void mousePressed(MouseEvent e) {
                button.setBorder(BorderFactory.createCompoundBorder(
                    BorderFactory.createLoweredBevelBorder(),
                    BorderFactory.createEmptyBorder(5, 10, 5, 10)));
            }
            
            @Override
            public void mouseReleased(MouseEvent e) {
                button.setBorder(BorderFactory.createCompoundBorder(
                    BorderFactory.createRaisedBevelBorder(),
                    BorderFactory.createEmptyBorder(5, 10, 5, 10)));
            }
        });
        
        return button;
    }
    
    private void setupKeyboardShortcuts() {
        // Ctrl+T for Take Screenshot
        getRootPane().registerKeyboardAction(
            e -> takeScreenshot(),
            KeyStroke.getKeyStroke(KeyEvent.VK_T, InputEvent.CTRL_DOWN_MASK),
            JComponent.WHEN_IN_FOCUSED_WINDOW
        );
        
        // Ctrl+S for Stop & Save
        getRootPane().registerKeyboardAction(
            e -> stopAndSave(),
            KeyStroke.getKeyStroke(KeyEvent.VK_S, InputEvent.CTRL_DOWN_MASK),
            JComponent.WHEN_IN_FOCUSED_WINDOW
        );
    }
    
    private void selectSavePath() {
        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setDialogTitle("Select Save Location");
        fileChooser.setFileFilter(new FileNameExtensionFilter("Word Documents (*.docx)", "docx"));
        
        // Set current directory from existing path
        File currentFile = new File(savePath);
        if (currentFile.getParentFile() != null && currentFile.getParentFile().exists()) {
            fileChooser.setCurrentDirectory(currentFile.getParentFile());
        }
        fileChooser.setSelectedFile(new File(savePath));
        
        int result = fileChooser.showSaveDialog(this);
        if (result == JFileChooser.APPROVE_OPTION) {
            File selectedFile = fileChooser.getSelectedFile();
            savePath = selectedFile.getAbsolutePath();
            if (!savePath.toLowerCase().endsWith(".docx")) {
                savePath += ".docx";
            }
            pathField.setText(savePath);
            pathField.setToolTipText(savePath);
            statusLabel.setText("Path set: " + selectedFile.getName());
        }
    }
    
    private void takeScreenshot() {
        try {
            // Minimize window before taking screenshot
            setState(Frame.ICONIFIED);
            Thread.sleep(500); // Wait for window to minimize
            
            // Capture the screen
            Robot robot = new Robot();
            Rectangle screenRect = new Rectangle(Toolkit.getDefaultToolkit().getScreenSize());
            BufferedImage screenshot = robot.createScreenCapture(screenRect);
            
            // Restore window
            setState(Frame.NORMAL);
            toFront();
            
            // Add to list
            stepNumber++;
            int currentStep = stepNumberCheckbox.isSelected() ? stepNumber : -1;
            screenshots.add(new ScreenshotEntry(screenshot, "", currentStep));
            
            updateCount();
            statusLabel.setText("Screenshot #" + stepNumber + " captured!");
            
            // Clear comment area for next screenshot
            commentArea.setText("");
            
        } catch (AWTException | InterruptedException ex) {
            setState(Frame.NORMAL);
            JOptionPane.showMessageDialog(this, 
                "Error capturing screenshot: " + ex.getMessage(),
                "Error", JOptionPane.ERROR_MESSAGE);
            statusLabel.setText("Error capturing.");
        }
    }
    
    private void addComment() {
        String comment = commentArea.getText().trim();
        if (comment.isEmpty()) {
            JOptionPane.showMessageDialog(this,
                "Please enter a comment first.",
                "No Comment", JOptionPane.WARNING_MESSAGE);
            return;
        }
        
        if (screenshots.isEmpty()) {
            // Add comment as standalone entry (no screenshot)
            stepNumber++;
            int currentStep = stepNumberCheckbox.isSelected() ? stepNumber : -1;
            screenshots.add(new ScreenshotEntry(null, comment, currentStep));
            updateCount();
            statusLabel.setText("Comment added as step " + stepNumber);
        } else {
            // Add comment to the last screenshot
            ScreenshotEntry lastEntry = screenshots.get(screenshots.size() - 1);
            if (lastEntry.comment.isEmpty()) {
                lastEntry.comment = comment;
                statusLabel.setText("Comment added to #" + screenshots.size());
            } else {
                // If last screenshot already has a comment, add as new entry
                stepNumber++;
                int currentStep = stepNumberCheckbox.isSelected() ? stepNumber : -1;
                screenshots.add(new ScreenshotEntry(null, comment, currentStep));
                updateCount();
                statusLabel.setText("Comment added as step " + stepNumber);
            }
        }
        
        commentArea.setText("");
    }
    
    private void stopAndSave() {
        if (screenshots.isEmpty()) {
            JOptionPane.showMessageDialog(this,
                "No screenshots to save.\nTake at least one screenshot first.",
                "Nothing to Save", JOptionPane.WARNING_MESSAGE);
            return;
        }
        
        // Verify save path is set
        if (savePath == null || savePath.trim().isEmpty()) {
            JOptionPane.showMessageDialog(this,
                "Please select a save location first.",
                "No Save Path", JOptionPane.WARNING_MESSAGE);
            selectSavePath();
            return;
        }
        
        statusLabel.setText("Saving...");
        
        try {
            saveToWord();
            
            // Verify file was created
            File savedFile = new File(savePath);
            if (savedFile.exists()) {
                JOptionPane.showMessageDialog(this,
                    "Document saved successfully!\n\nLocation:\n" + savePath + 
                    "\n\nSize: " + (savedFile.length() / 1024) + " KB",
                    "Success", JOptionPane.INFORMATION_MESSAGE);
                statusLabel.setText("Saved: " + savedFile.getName());
            } else {
                throw new IOException("File was not created at the specified location.");
            }
            
            // Ask if user wants to continue or exit
            int choice = JOptionPane.showConfirmDialog(this,
                "Document saved. Start a new session?",
                "Continue?", JOptionPane.YES_NO_OPTION);
            
            if (choice == JOptionPane.YES_OPTION) {
                clearAll();
            } else {
                System.exit(0);
            }
            
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this,
                "Error saving document:\n" + ex.getMessage() + 
                "\n\nTried to save to:\n" + savePath,
                "Error", JOptionPane.ERROR_MESSAGE);
            statusLabel.setText("Error saving!");
            ex.printStackTrace();
        }
    }
    
    private void saveToWord() throws Exception {
        // Ensure parent directory exists
        File outputFile = new File(savePath);
        File parentDir = outputFile.getParentFile();
        if (parentDir != null && !parentDir.exists()) {
            boolean created = parentDir.mkdirs();
            if (!created) {
                throw new IOException("Could not create directory: " + parentDir.getAbsolutePath());
            }
        }
        
        // Check if we can write to the location
        if (outputFile.exists() && !outputFile.canWrite()) {
            throw new IOException("Cannot write to file (file may be open or read-only): " + savePath);
        }
        
        XWPFDocument document = new XWPFDocument();
        
        try {
            // Add title
            XWPFParagraph titlePara = document.createParagraph();
            titlePara.setAlignment(ParagraphAlignment.CENTER);
            XWPFRun titleRun = titlePara.createRun();
            titleRun.setText("Screenshot Documentation");
            titleRun.setBold(true);
            titleRun.setFontSize(18);
            titleRun.addBreak();
            titleRun.addBreak();
            
            // Add timestamp
            XWPFParagraph datePara = document.createParagraph();
            datePara.setAlignment(ParagraphAlignment.CENTER);
            XWPFRun dateRun = datePara.createRun();
            dateRun.setText("Generated: " + new java.util.Date().toString());
            dateRun.setItalic(true);
            dateRun.setFontSize(10);
            dateRun.addBreak();
            
            // Add branding
            XWPFRun brandRun = datePara.createRun();
            brandRun.setText(DESIGNED_BY);
            brandRun.setItalic(true);
            brandRun.setFontSize(9);
            brandRun.addBreak();
            brandRun.addBreak();
            
            // Add each screenshot entry
            for (ScreenshotEntry entry : screenshots) {
                XWPFParagraph para = document.createParagraph();
                
                // Add step number if enabled
                if (entry.stepNum > 0) {
                    XWPFRun stepRun = para.createRun();
                    stepRun.setText("Step " + entry.stepNum + ":");
                    stepRun.setBold(true);
                    stepRun.setFontSize(12);
                    stepRun.addBreak();
                }
                
                // Add comment if present
                if (entry.comment != null && !entry.comment.isEmpty()) {
                    XWPFRun commentRun = para.createRun();
                    commentRun.setText(entry.comment);
                    commentRun.setFontSize(11);
                    commentRun.addBreak();
                    commentRun.addBreak();
                }
                
                // Add screenshot if present
                if (entry.image != null) {
                    // Convert BufferedImage to byte array
                    ByteArrayOutputStream baos = new ByteArrayOutputStream();
                    ImageIO.write(entry.image, "png", baos);
                    byte[] imageBytes = baos.toByteArray();
                    baos.close();
                    
                    // Calculate dimensions to fit page width (max 6 inches wide)
                    int imgWidth = entry.image.getWidth();
                    int imgHeight = entry.image.getHeight();
                    
                    // Max width is 6 inches, calculate scale
                    double maxWidthInches = 6.0;
                    double imgWidthInches = imgWidth / 96.0; // Assuming 96 DPI screen
                    double scale = 1.0;
                    if (imgWidthInches > maxWidthInches) {
                        scale = maxWidthInches / imgWidthInches;
                    }
                    
                    // Calculate final dimensions in inches
                    double finalWidthInches = (imgWidth / 96.0) * scale;
                    double finalHeightInches = (imgHeight / 96.0) * scale;
                    
                    // Convert inches to EMUs (1 inch = 914400 EMUs)
                    int widthEMU = (int)(finalWidthInches * 914400);
                    int heightEMU = (int)(finalHeightInches * 914400);
                    
                    XWPFRun imageRun = para.createRun();
                    ByteArrayInputStream bais = new ByteArrayInputStream(imageBytes);
                    imageRun.addPicture(
                        bais,
                        XWPFDocument.PICTURE_TYPE_PNG,
                        "screenshot.png",
                        widthEMU,
                        heightEMU
                    );
                    bais.close();
                    imageRun.addBreak();
                }
                
                // Add separator
                XWPFParagraph sepPara = document.createParagraph();
                XWPFRun sepRun = sepPara.createRun();
                sepRun.setText("────────────────────────────────────────────");
                sepRun.addBreak();
            }
            
            // Write to file
            try (FileOutputStream fos = new FileOutputStream(outputFile)) {
                document.write(fos);
                fos.flush();
            }
            
        } finally {
            document.close();
        }
    }
    
    private void clearAll() {
        screenshots.clear();
        stepNumber = 0;
        commentArea.setText("");
        updateCount();
        statusLabel.setText("Cleared. Ready.");
    }
    
    private void updateCount() {
        countLabel.setText("Count: " + screenshots.size());
    }
    
    public static void main(String[] args) {
        // Set look and feel to system native
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception e) {
            // Use default look and feel
        }
        
        // Run on EDT
        SwingUtilities.invokeLater(() -> {
            ScreenshotTool tool = new ScreenshotTool();
            tool.setVisible(true);
        });
    }
}
