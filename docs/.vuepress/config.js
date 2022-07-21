module.exports = {
  base: '/mini_jx3_bot/',
  title: '团子机器人',
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
            ['/guide/', '部署机器人'],
            ['/guide/config', '设置配置'],
            ['/guide/setting', '启动机器人'],
          ]
        }
      ],
      '/development/': [
        {
          title: '开发手册',
        }
      ]
    }
  },
  description: '一个女生自用的剑网三机器人，内置了部分插件，欢迎二次开发！'
}
