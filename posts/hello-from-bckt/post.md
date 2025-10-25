---
title: "Welcome to Your bckt Blog"
slug: "welcome"
date: "2025-01-01T00:00:00Z"
tags:
  - welcome
  - github-pages
abstract: "Your blog is now live on GitHub Pages, powered by bckt."
attached: []
images: []
---

Congratulations! Your blog is now live and automatically deployed to GitHub Pages.

## What just happened?

Every time you push changes to your repository, GitHub Actions automatically:

1. Downloads the latest bckt release
2. Renders your markdown posts into a beautiful static site
3. Deploys it to GitHub Pages

## Getting Started

To create a new post, you can either:

- Create a new folder under `posts/` with a `post.md` file
- Use `bckt-new` locally (if you have bckt installed)
- Write directly in GitHub's web editor

### Post Structure

Each post needs YAML frontmatter at the top:

```yaml
---
title: "My Post Title"
slug: "my-post-slug"
date: "2025-01-01T12:00:00Z"
tags:
  - tag1
  - tag2
abstract: "A brief description of your post"
---
```

Then write your content in Markdown below the frontmatter.

## Customization

Edit `bckt.yaml` to customize your site:

- Update the `title` and `description`
- Change the `base_url` to match your GitHub Pages URL
- Adjust `homepage_posts` to control how many posts appear on the homepage

## Version Pinning

By default, your site uses the latest bckt release. To pin to a specific version, create a `.bckt-version` file in the root:

```bash
echo "v0.6.2" > .bckt-version
```

## Learn More

- [bckt Documentation](https://github.com/vrypan/bckt)
- [GitHub Pages Setup Guide](https://github.com/vrypan/bckt/blob/main/docs/github-pages-setup.md)
- [MiniJinja Template Syntax](https://docs.rs/minijinja/)

Happy blogging!
