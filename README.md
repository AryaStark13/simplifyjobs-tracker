# 🎯 New Grad Job Application Tracker

A lightweight, browser-based application for tracking your 2026 New Graduate job applications. This tool automatically pulls the latest job listings from the [SimplifyJobs New-Grad-Positions repository](https://github.com/SimplifyJobs/New-Grad-Positions) and helps you manage your application pipeline with status tracking and progress monitoring.

## ✨ Features

- **Automatic Job Updates**: Fetches latest positions from SimplifyJobs repository
- **Application Tracking**: Mark jobs as applied and track your progress through the interview process
- **Status Management**: Track applications from "Not Applied" to "Offer" (or "Ghosted")
- **Smart Filtering**: Filter by application status, search by company/role/location
- **Progress Analytics**: Visual statistics showing your application progress
- **Responsive Design**: Works on desktop and mobile devices
- **Offline Support**: Cached data works even when offline
- **Auto-Ghosting**: Automatically marks applications as "Ghosted" after 3 months of no updates

## 🚀 How to Use

### Getting Started
1. **Open the application** in your web browser
2. **Click "Update Jobs"** to fetch the latest positions from SimplifyJobs
3. **Browse through job categories**:
   - 🤖 AI/ML Roles
   - 💻 Software Engineering Roles  
   - 📈 Quantitative Finance Roles
   - 🔧 Hardware Engineering Roles

### Tracking Applications
1. **Check the checkbox** next to jobs you've applied to
2. **Update the status dropdown** as you progress:
   - Not Applied → Applied → OA Received → OA Solved → Interview Call → Offer
   - Or mark as "Rejected" if unsuccessful
3. **Use the search bar** to find specific companies or roles
4. **Filter by status** using the filter buttons to focus on specific stages

### Understanding the Interface
- **🛂 Symbol**: Position does not offer visa sponsorship
- **🇺🇸 Symbol**: Position requires U.S. citizenship
- **🔒 Symbol**: Job application is closed (these are automatically filtered out)
- **Green highlighting**: Rows for jobs you've applied to
- **Age column**: How long ago the job was posted
- **Apply button**: Direct link to the job application

## 📊 Data Storage & Persistence

### How Your Data is Stored
Your application data is stored locally in your browser using **localStorage**. This includes:
- Which jobs you've marked as applied
- Status updates for each application
- Timestamp of last status change
- Collapsed/expanded section preferences

### Why Your Data Won't Disappear
- **Local Storage**: Data persists across browser sessions
- **No Account Required**: No dependency on external services or logins
- **Automatic Caching**: Job listings are cached locally for offline access
- **Cross-Session Persistence**: Your tracking data remains even if you close the browser

### When Your Data MIGHT Disappear
⚠️ **Important Limitations to Understand:**

1. **Browser Data Clearing**:
   - Manually clearing browser data/cookies will erase your tracking
   - Using "Clear browsing data" in browser settings
   - Privacy-focused browser extensions that clear data

2. **Incognito/Private Browsing**:
   - Data will NOT persist when using private/incognito mode
   - Always use regular browser sessions for tracking

3. **Different Browsers/Devices**:
   - Data is tied to specific browser on specific device
   - Switching from Chrome to Firefox = separate data
   - Using different computers = separate tracking

4. **Browser Storage Limits**:
   - Extremely rare, but browsers can clear localStorage if storage quota is exceeded
   - Modern browsers typically allow 5-10MB per domain

5. **Browser Updates/Corruption**:
   - Very rare, but major browser updates or profile corruption could affect data

### Best Practices for Data Safety
- **Use the same browser** consistently for tracking
- **Bookmark the application** for easy access
- **Periodically export** your progress (take screenshots of statistics)
- **Don't rely solely** on this tool - keep a backup spreadsheet for critical applications

## 🔄 Data Sources

This application pulls job data from:
- **Primary Source**: [SimplifyJobs New-Grad-Positions Repository](https://github.com/SimplifyJobs/New-Grad-Positions)
- **Update Frequency**: Manual refresh or automatic every 30 minutes
- **Data Freshness**: Jobs are pulled from the latest commit on the `dev` branch

### About SimplifyJobs
[SimplifyJobs](https://github.com/SimplifyJobs) maintains one of the most comprehensive, up-to-date lists of new graduate positions. The repository is community-driven and updated frequently with new opportunities across multiple engineering disciplines.

## 🛠️ Technical Details

- **Framework**: Vanilla HTML/CSS/JavaScript (no dependencies)
- **Storage**: Browser localStorage API
- **Data Source**: GitHub raw content API
- **Offline Support**: Cached job listings work without internet
- **Performance**: Lightweight single-file application (~50KB)

## 📱 Browser Compatibility

- ✅ Chrome/Chromium (recommended)
- ✅ Firefox  
- ✅ Safari
- ✅ Edge
- ⚠️ Internet Explorer (not recommended)

## 🤝 Contributing

This is a client-side only application. To contribute:
1. Fork this repository
2. Make your changes to the HTML file
3. Test locally by opening in browser
4. Submit a pull request

## 📄 License

This project is open source. The job data is sourced from the SimplifyJobs repository under their respective license terms.

## 🆘 Support

If you encounter issues:
1. **Refresh the page** and try updating jobs again
2. **Clear browser cache** if data seems corrupted
3. **Check browser console** for error messages
4. **Verify internet connection** for job updates

---

**Note**: This tool is not affiliated with SimplifyJobs but gratefully uses their publicly available job data to help new graduates track their applications more effectively.