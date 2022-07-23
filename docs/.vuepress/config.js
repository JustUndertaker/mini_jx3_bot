module.exports = {
  base: '/mini_jx3_bot/',
  title: '团子机器人',
  plugins: ['@vuepress/last-updated'],
  head: [
    ['link', { rel: 'icon', href: '/favicon.png' }],
  ],
  markdown: {
    lineNumbers: true // 代码块显示行号
  },
  themeConfig: {
    logo: 'logo.png',
    sidebarDepth: 2,
    lastUpdated: 'Last Updated',
    nav: [
      { text: '用户文档', link: '/guide/' },
      { text: '开发手册', link: '/development/' },
      { text: 'Github', link: 'https://github.com/JustUndertaker/mini_jx3_bot' }
    ],
    sidebar: {
      '/guide/': [
        {
          title: '用户文档',
          sidebarDepth: 2,
          children: [
            ['/guide/', '项目说明'],
            ['/guide/deploy', '部署机器人'],
            ['/guide/meau', '功能列表'],
            ['/guide/question', '常见问题'],
            ['/guide/about', '作者的话']
          ]
        }
      ],
      '/development/': [
        {
          title: '开发手册',
          sidebarDepth: 2,
          children: [
            ['/development/', '开发说明'],
            ['/development/environment', '环境安装'],
            ['/development/plugin', '编写插件'],
            ['/development/other', '其他工具'],
          ]
        }
      ]
    }
  },
  description: '一个女生自用的剑网三机器人，内置了部分插件，欢迎二次开发！'
}
