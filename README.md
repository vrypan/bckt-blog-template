# bckt Blog Template

A ready-to-use blog template powered by [bckt](https://github.com/vrypan/bckt) and automatically deployed to GitHub Pages.

## Features

- **Zero installation required** - Just write markdown and push
- **Automatic deployment** - GitHub Actions handles everything
- **Auto-updating** - Always uses the latest bckt release (or pin to a specific version)
- **Clean, responsive theme** - Beautiful out of the box
- **Client-side search** - Built-in search functionality

## Quick Start

### 1. Create Your Repository

Click the **"Use this template"** button at the top of this repository, then:

- Choose a repository name (e.g., `my-blog`)
- Make it public (required for GitHub Pages on free accounts)
- Click **"Create repository from template"**

### 2. Enable GitHub Pages

1. Go to your new repository's **Settings** → **Pages**
2. Under **Source**, select **"GitHub Actions"**
3. Save

### 3. Configure Your Site

Edit `bckt.yaml`:

```yaml
title: "Your Blog Name"
description: "Your blog description"
base_url: "https://yourusername.github.io/your-repo-name"
```

Push your changes, and GitHub Actions will automatically deploy your site!

### 4. Start Writing

Create new posts in the `posts/` directory. Each post should be in its own folder with a `post.md` file:

```
posts/
  my-first-post/
    post.md
```

Post format:

```markdown
---
title: "My First Post"
slug: "my-first-post"
date: "2025-01-15T12:00:00Z"
tags:
  - blogging
abstract: "A brief description of your post"
---

Your content here in Markdown format...
```

Push to GitHub, and your site will rebuild automatically!

## Writing Posts

### In GitHub's Web Editor

1. Navigate to `posts/` in your repository
2. Click **"Add file"** → **"Create new file"**
3. Name it `posts/my-post-title/post.md`
4. Add frontmatter and content
5. Commit directly to main

### Locally (Optional)

If you want to preview locally:

```bash
# Install bckt
curl -L https://github.com/vrypan/bckt/releases/latest/download/bckt-[your-platform].tar.gz | tar xz

# Create a new post
bckt-new --title "My Post"

# Preview locally
bckt dev

# When ready, commit and push
git add .
git commit -m "Add new post"
git push
```

## Customization

### Site Settings

Edit `bckt.yaml` to customize:

- `title` - Your site name
- `description` - Site description (used in meta tags)
- `base_url` - Your GitHub Pages URL
- `homepage_posts` - Number of posts on the homepage
- `date_format` - How dates are displayed

### Theme

The default theme is `bckt3`. You can customize it by editing files in the `themes/bckt3/` directory, or create your own theme. See [bckt documentation](https://github.com/vrypan/bckt/blob/main/docs/README.md) for details.

### Custom Domain

To use a custom domain:

1. Add a `CNAME` file to the `skel/` directory with your domain:
   ```bash
   echo "blog.yourdomain.com" > skel/CNAME
   ```

2. Configure DNS:
   - Add a CNAME record pointing to `yourusername.github.io`

3. In GitHub Settings → Pages, add your custom domain

## Version Pinning

By default, the workflow uses the latest bckt release. To pin to a specific version:

```bash
echo "v0.6.2" > .bckt-version
git add .bckt-version
git commit -m "Pin bckt version"
git push
```

To switch back to auto-updating, delete the `.bckt-version` file.

## How It Works

Every time you push to the `main` branch, GitHub Actions:

1. Checks out your repository
2. Downloads bckt (latest or pinned version)
3. Runs `bckt render` to generate HTML
4. Deploys the `html/` directory to GitHub Pages

The workflow file is at `.github/workflows/deploy.yml`.

## Repository Structure

```
.
├── .github/
│   └── workflows/
│       └── deploy.yml       # GitHub Actions workflow
├── posts/                   # Your blog posts go here
│   └── hello-from-bckt/
│       └── post.md
├── themes/
│   └── bckt3/              # Default theme
├── skel/                   # Static assets (copied to output)
├── bckt.yaml               # Site configuration
├── .gitignore
└── README.md
```

## Troubleshooting

### Site Not Updating

1. Check the **Actions** tab for errors
2. Verify GitHub Pages source is set to "GitHub Actions"
3. Clear your browser cache

### Build Failures

Common issues:

- Invalid YAML frontmatter in posts
- Missing required fields (title, slug, date)
- Invalid date format (use ISO 8601: `YYYY-MM-DDTHH:MM:SSZ`)

Check the Actions tab for detailed error messages.

## Examples

- [blog.vrypan.net](https://blog.vrypan.net/) - Personal blog using bckt
- [steve.photo](https://steve.photo) - Photography site with bckt-photo

## Resources

- [bckt Documentation](https://github.com/vrypan/bckt/blob/main/docs/README.md)
- [GitHub Pages Setup Guide](https://github.com/vrypan/bckt/blob/main/docs/github-pages-setup.md)
- [Report Issues](https://github.com/vrypan/bckt/issues)

## License

This template is free to use. bckt is licensed under the MIT License.

---

**Happy blogging!** Questions? [Open an issue](https://github.com/vrypan/bckt/issues).
