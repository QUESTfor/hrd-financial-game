# ☁️ Streamlit Cloud Deployment - Quick Checklist

## ✅ Pre-Deployment Checklist

### **Files You Need:**

- [ ] `app.py` - Your main game code
- [ ] `requirements.txt` - Package dependencies  
- [ ] `firebase-key.json` - Firebase credentials
- [ ] `.gitignore` (optional) - Exclude sensitive files

---

## 📝 requirements.txt

```txt
streamlit==1.31.0
plotly==5.18.0
firebase-admin==6.4.0
numpy==1.26.3
scipy==1.11.4
```

**Save this as `requirements.txt` in your project folder**

---

## 🚀 5-Minute Deployment

### **Step 1: Create GitHub Repo (2 min)**

1. Go to https://github.com/new
2. Repository name: `hrd-financial-game`
3. Make it **Public**
4. ✅ Add README
5. Click "Create repository"

---

### **Step 2: Upload Files (2 min)**

1. Click "Add file" → "Upload files"
2. Upload these 3 files:
   - ✅ app.py
   - ✅ requirements.txt
   - ✅ firebase-key.json
3. Click "Commit changes"

---

### **Step 3: Deploy (1 min)**

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select:
   - Repository: `your-username/hrd-financial-game`
   - Branch: `main`
   - Main file: `app.py`
5. Click "Deploy!"

---

## ⏰ Wait 2-3 minutes...

**Your app is building!**

You'll see:
```
🔨 Building...
📦 Installing packages...
🚀 Starting app...
✅ Your app is live!
```

---

## 🎉 You're Live!

**Your permanent URL:**
```
https://your-username-hrd-financial-game.streamlit.app
```

**Share this with students!**

---

## 🔒 Optional: Secure Firebase Credentials

### **Better Security (Recommended):**

1. **Remove firebase-key.json from GitHub**
   ```
   GitHub → Your Repo → firebase-key.json → Delete file
   ```

2. **Add to Streamlit Secrets**
   ```
   Streamlit Cloud → Your App → Settings → Secrets
   → Paste your firebase JSON content
   ```

3. **Update app.py**
   ```python
   # Change this line:
   cred = credentials.Certificate('firebase-key.json')
   
   # To this:
   import json
   firebase_config = json.loads(st.secrets["firebase"])
   cred = credentials.Certificate(firebase_config)
   ```

---

## 🛠️ Managing Your App

### **Update Code:**
```bash
# Edit app.py locally
git add app.py
git commit -m "Update feature"
git push

# Streamlit Cloud auto-deploys! ✅
```

### **View Logs:**
```
Streamlit Cloud → Your App → Logs
```

### **Restart App:**
```
Streamlit Cloud → Your App → ⋮ → Reboot
```

---

## 🆘 Troubleshooting

### **Error: Requirements not found**
✅ Make sure `requirements.txt` is in root folder

### **Error: Firebase authentication failed**  
✅ Check firebase-key.json is uploaded
✅ Or use Streamlit Secrets

### **App won't start**
✅ Check logs for error messages
✅ Verify all files uploaded correctly

### **App is slow**
✅ Normal on first load (cold start)
✅ Fast after initial load
✅ Add caching to improve speed

---

## 💰 Cost

**FREE Forever!**
- ✅ Unlimited visitors
- ✅ 1 GB RAM
- ✅ 24/7 uptime
- ✅ Community support

**Perfect for classroom use!** 🎓

---

## 🎯 Final Checklist

- [ ] GitHub repo created
- [ ] Files uploaded (app.py, requirements.txt, firebase-key.json)
- [ ] App deployed on Streamlit Cloud
- [ ] Permanent URL obtained
- [ ] URL shared with students
- [ ] Admin password shared with teachers
- [ ] Test login works
- [ ] Test game functionality
- [ ] Bookmark admin dashboard

---

## 🎉 You're Done!

**Your game is now:**
- ✅ Live 24/7
- ✅ Accessible anywhere
- ✅ Permanent URL
- ✅ Professional deployment
- ✅ Still 100% FREE!

**Share your URL and start teaching!** 🚀📊💰
