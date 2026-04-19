import javax.swing.*;
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
 * Features:
 * - Take Screenshot: Captures full screen
 * - Add Comment: Adds text comment with the screenshot
 * - Stop: Saves all screenshots to Word document
 * - Browse: Select save path
 * - Step Number checkbox: Adds step numbers if checked
 */
public class ScreenshotTool extends JFrame {
    
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
        super("Screenshot Tool");
        screenshots = new ArrayList<>();
        stepNumber = 0;
        savePath = System.getProperty("user.home") + File.separator + "Screenshots.docx";
        
        initializeUI();
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(500, 400);
        setLocationRelativeTo(null);
        setResizable(true);
    }
    
    private void initializeUI() {
        // Main panel with padding
        JPanel mainPanel = new JPanel(new BorderLayout(10, 10));
        mainPanel.setBorder(BorderFactory.createEmptyBorder(15, 15, 15, 15));
        
        // Top panel - Path selection
        JPanel pathPanel = new JPanel(new BorderLayout(5, 0));
        pathPanel.setBorder(BorderFactory.createTitledBorder("Save Location"));
        
        pathField = new JTextField(savePath);
        pathField.setEditable(false);
        JButton browseButton = new JButton("Browse...");
        browseButton.addActionListener(e -> selectSavePath());
        
        pathPanel.add(pathField, BorderLayout.CENTER);
        pathPanel.add(browseButton, BorderLayout.EAST);
        
        // Center panel - Comment area and checkbox
        JPanel centerPanel = new JPanel(new BorderLayout(5, 5));
        centerPanel.setBorder(BorderFactory.createTitledBorder("Comment (Optional)"));
        
        commentArea = new JTextArea(4, 30);
        commentArea.setLineWrap(true);
        commentArea.setWrapStyleWord(true);
        JScrollPane scrollPane = new JScrollPane(commentArea);
        
        stepNumberCheckbox = new JCheckBox("Add Step Numbers", true);
        
        centerPanel.add(scrollPane, BorderLayout.CENTER);
        centerPanel.add(stepNumberCheckbox, BorderLayout.SOUTH);
        
        // Button panel
        JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.CENTER, 10, 5));
        
        JButton takeScreenshotBtn = new JButton("Take Screenshot");
        takeScreenshotBtn.setBackground(new Color(76, 175, 80));
        takeScreenshotBtn.setForeground(Color.WHITE);
        takeScreenshotBtn.setFocusPainted(false);
        takeScreenshotBtn.addActionListener(e -> takeScreenshot());
        
        JButton addCommentBtn = new JButton("Add Comment");
        addCommentBtn.setBackground(new Color(33, 150, 243));
        addCommentBtn.setForeground(Color.WHITE);
        addCommentBtn.setFocusPainted(false);
        addCommentBtn.addActionListener(e -> addComment());
        
        JButton stopBtn = new JButton("Stop & Save");
        stopBtn.setBackground(new Color(244, 67, 54));
        stopBtn.setForeground(Color.WHITE);
        stopBtn.setFocusPainted(false);
        stopBtn.addActionListener(e -> stopAndSave());
        
        JButton clearBtn = new JButton("Clear All");
        clearBtn.addActionListener(e -> clearAll());
        
        buttonPanel.add(takeScreenshotBtn);
        buttonPanel.add(addCommentBtn);
        buttonPanel.add(stopBtn);
        buttonPanel.add(clearBtn);
        
        // Status panel
        JPanel statusPanel = new JPanel(new BorderLayout());
        statusLabel = new JLabel("Ready. Click 'Take Screenshot' to capture.");
        countLabel = new JLabel("Screenshots: 0");
        statusPanel.add(statusLabel, BorderLayout.WEST);
        statusPanel.add(countLabel, BorderLayout.EAST);
        
        // Assemble main panel
        JPanel topContainer = new JPanel(new BorderLayout(0, 10));
        topContainer.add(pathPanel, BorderLayout.NORTH);
        topContainer.add(centerPanel, BorderLayout.CENTER);
        
        mainPanel.add(topContainer, BorderLayout.NORTH);
        mainPanel.add(buttonPanel, BorderLayout.CENTER);
        mainPanel.add(statusPanel, BorderLayout.SOUTH);
        
        add(mainPanel);
    }
    
    private void selectSavePath() {
        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setDialogTitle("Select Save Location");
        fileChooser.setFileFilter(new FileNameExtensionFilter("Word Documents (*.docx)", "docx"));
        fileChooser.setSelectedFile(new File(savePath));
        
        int result = fileChooser.showSaveDialog(this);
        if (result == JFileChooser.APPROVE_OPTION) {
            File selectedFile = fileChooser.getSelectedFile();
            savePath = selectedFile.getAbsolutePath();
            if (!savePath.toLowerCase().endsWith(".docx")) {
                savePath += ".docx";
            }
            pathField.setText(savePath);
            statusLabel.setText("Save path updated.");
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
            
            // Add to list
            stepNumber++;
            int currentStep = stepNumberCheckbox.isSelected() ? stepNumber : -1;
            screenshots.add(new ScreenshotEntry(screenshot, "", currentStep));
            
            updateCount();
            statusLabel.setText("Screenshot " + stepNumber + " captured successfully!");
            
            // Clear comment area for next screenshot
            commentArea.setText("");
            
        } catch (AWTException | InterruptedException ex) {
            setState(Frame.NORMAL);
            JOptionPane.showMessageDialog(this, 
                "Error capturing screenshot: " + ex.getMessage(),
                "Error", JOptionPane.ERROR_MESSAGE);
            statusLabel.setText("Error capturing screenshot.");
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
                statusLabel.setText("Comment added to screenshot " + screenshots.size());
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
                "No screenshots to save. Take at least one screenshot first.",
                "Nothing to Save", JOptionPane.WARNING_MESSAGE);
            return;
        }
        
        statusLabel.setText("Saving document...");
        
        try {
            saveToWord();
            JOptionPane.showMessageDialog(this,
                "Document saved successfully!\n" + savePath,
                "Success", JOptionPane.INFORMATION_MESSAGE);
            statusLabel.setText("Document saved: " + savePath);
            
            // Ask if user wants to continue or exit
            int choice = JOptionPane.showConfirmDialog(this,
                "Document saved. Do you want to start a new session?",
                "Continue?", JOptionPane.YES_NO_OPTION);
            
            if (choice == JOptionPane.YES_OPTION) {
                clearAll();
            } else {
                System.exit(0);
            }
            
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this,
                "Error saving document: " + ex.getMessage(),
                "Error", JOptionPane.ERROR_MESSAGE);
            statusLabel.setText("Error saving document.");
            ex.printStackTrace();
        }
    }
    
    private void saveToWord() throws Exception {
        XWPFDocument document = new XWPFDocument();
        
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
        dateRun.addBreak();
        
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
                
                // Calculate dimensions to fit page width (max 6 inches wide)
                int width = entry.image.getWidth();
                int height = entry.image.getHeight();
                double maxWidth = 6.0 * 72; // 6 inches in points
                double scale = maxWidth / width;
                if (scale > 1) scale = 1; // Don't enlarge
                
                int finalWidth = (int)(width * scale);
                int finalHeight = (int)(height * scale);
                
                XWPFRun imageRun = para.createRun();
                imageRun.addPicture(
                    new ByteArrayInputStream(imageBytes),
                    XWPFDocument.PICTURE_TYPE_PNG,
                    "screenshot.png",
                    Units.toEMU(finalWidth * 72.0 / 96), // Convert pixels to EMUs
                    Units.toEMU(finalHeight * 72.0 / 96)
                );
                imageRun.addBreak();
            }
            
            // Add separator
            XWPFParagraph sepPara = document.createParagraph();
            XWPFRun sepRun = sepPara.createRun();
            sepRun.setText("─".repeat(50));
            sepRun.addBreak();
        }
        
        // Save the document
        File outputFile = new File(savePath);
        outputFile.getParentFile().mkdirs(); // Create directories if needed
        
        try (FileOutputStream fos = new FileOutputStream(outputFile)) {
            document.write(fos);
        }
        
        document.close();
    }
    
    private void clearAll() {
        screenshots.clear();
        stepNumber = 0;
        commentArea.setText("");
        updateCount();
        statusLabel.setText("Cleared. Ready for new session.");
    }
    
    private void updateCount() {
        countLabel.setText("Screenshots: " + screenshots.size());
    }
    
    public static void main(String[] args) {
        // Set look and feel
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
