# Put your demo video here

Name it **`demo.mp4`** and it appears in the *Watch it work* section automatically.
Nothing in the code needs changing.

```
presentation/site/video/demo.mp4
```

The file is **gitignored on purpose.** GitHub rejects any file over 100 MB, and this
repository's history is already ~1.7 GB from the committed `.deb` packages. The video
travels with the folder, not with git.

## Compress it first — 500 MB is far too big

A screen recording that size is almost always uncompressed or badly encoded. This
typically takes it to 20–60 MB with no visible quality loss:

```bash
ffmpeg -i your-recording.mov \
  -vf "scale=1920:-2" \
  -c:v libx264 -crf 24 -preset slow -pix_fmt yuv420p \
  -c:a aac -b:a 128k \
  -movflags +faststart \
  demo.mp4
```

- `-crf 24` is the quality dial. Raise to `28` for a smaller file, drop to `20` for better.
- `-movflags +faststart` matters — without it the browser must download the whole file
  before it can start playing.
- `-pix_fmt yuv420p` keeps it playable in Safari and Firefox, not just Chrome.
- Still too big? Add `-r 30` to cap the frame rate, or scale to `1280:-2`.

Check the result: `ls -lh demo.mp4`

## Trim it too

For a talk, 60–90 seconds is plenty. Cut before compressing:

```bash
ffmpeg -ss 00:00:12 -to 00:01:35 -i your-recording.mov -c copy trimmed.mov
```

## If you would rather stream it

Upload to YouTube as **unlisted**, then set the `embed` field in
`site-src/src/App.jsx`:

```js
const VIDEO = {
  src: 'video/demo.mp4',
  poster: 'shots/app-02-authenticated.png',
  embed: 'https://www.youtube.com/embed/YOUR_ID',   // local file is ignored when set
};
```

Rebuild afterwards (`npm run build` in `site-src/`, then copy `dist/` over `site/`).

**For the actual presentation, prefer the local file.** It needs no network, so bad wifi
in the room cannot take your demo down.

## No video yet?

The section renders a dashed placeholder explaining what is missing, so the site never
shows a broken player.
