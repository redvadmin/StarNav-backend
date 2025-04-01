from django.db import migrations

def add_preset_navigations(apps, schema_editor):
    Category = apps.get_model('core', 'Category')
    Navigation = apps.get_model('core', 'Navigation')
    
    # 创建分类
    categories = {
        '常用': Category.objects.create(name='常用', icon='mdi-star', order=1),
        '工作': Category.objects.create(name='工作', icon='mdi-briefcase', order=2),
        '学习': Category.objects.create(name='学习', icon='mdi-book-open-variant', order=3),
        '娱乐': Category.objects.create(name='娱乐', icon='mdi-gamepad-variant', order=4),
        '工具': Category.objects.create(name='工具', icon='mdi-tools', order=5),
        '社交': Category.objects.create(name='社交', icon='mdi-account-group', order=6),
        '健康': Category.objects.create(name='健康', icon='mdi-heart-pulse', order=7),
    }
    
    # 预置导航数据
    navigations = [
        # 常用
        {'title': 'Google', 'url': 'https://www.google.com', 'category': categories['常用'], 'description': '全球最大的搜索引擎', 'order': 1},
        {'title': 'GitHub', 'url': 'https://github.com', 'category': categories['常用'], 'description': '全球最大的代码托管平台', 'order': 2},
        {'title': 'ChatGPT', 'url': 'https://chat.openai.com', 'category': categories['常用'], 'description': 'OpenAI开发的AI对话模型', 'order': 3},
        {'title': 'YouTube', 'url': 'https://www.youtube.com', 'category': categories['常用'], 'description': '全球最大的视频分享平台', 'order': 4},
        {'title': 'Reddit', 'url': 'https://www.reddit.com', 'category': categories['常用'], 'description': '全球最大的社交新闻网站', 'order': 5},
        
        # 工作
        {'title': 'LinkedIn', 'url': 'https://www.linkedin.com', 'category': categories['工作'], 'description': '职业社交网络', 'order': 1},
        {'title': 'Slack', 'url': 'https://slack.com', 'category': categories['工作'], 'description': '团队协作工具', 'order': 2},
        {'title': 'Trello', 'url': 'https://trello.com', 'category': categories['工作'], 'description': '项目管理工具', 'order': 3},
        {'title': 'Notion', 'url': 'https://www.notion.so', 'category': categories['工作'], 'description': '笔记和知识管理工具', 'order': 4},
        {'title': 'Figma', 'url': 'https://www.figma.com', 'category': categories['工作'], 'description': '设计协作工具', 'order': 5},
        
        # 学习
        {'title': 'Coursera', 'url': 'https://www.coursera.org', 'category': categories['学习'], 'description': '在线教育平台', 'order': 1},
        {'title': 'Udemy', 'url': 'https://www.udemy.com', 'category': categories['学习'], 'description': '技能学习平台', 'order': 2},
        {'title': 'Duolingo', 'url': 'https://www.duolingo.com', 'category': categories['学习'], 'description': '语言学习平台', 'order': 3},
        {'title': 'Stack Overflow', 'url': 'https://stackoverflow.com', 'category': categories['学习'], 'description': '程序员问答社区', 'order': 4},
        {'title': 'MDN Web Docs', 'url': 'https://developer.mozilla.org', 'category': categories['学习'], 'description': 'Web开发文档', 'order': 5},
        
        # 娱乐
        {'title': 'Netflix', 'url': 'https://www.netflix.com', 'category': categories['娱乐'], 'description': '流媒体视频服务', 'order': 1},
        {'title': 'Spotify', 'url': 'https://www.spotify.com', 'category': categories['娱乐'], 'description': '音乐流媒体服务', 'order': 2},
        {'title': 'Twitch', 'url': 'https://www.twitch.tv', 'category': categories['娱乐'], 'description': '游戏直播平台', 'order': 3},
        {'title': 'Steam', 'url': 'https://store.steampowered.com', 'category': categories['娱乐'], 'description': '游戏平台', 'order': 4},
        {'title': 'Pinterest', 'url': 'https://www.pinterest.com', 'category': categories['娱乐'], 'description': '图片分享平台', 'order': 5},
        
        # 工具
        {'title': 'Canva', 'url': 'https://www.canva.com', 'category': categories['工具'], 'description': '在线设计工具', 'order': 1},
        {'title': 'Grammarly', 'url': 'https://www.grammarly.com', 'category': categories['工具'], 'description': '写作助手', 'order': 2},
        {'title': 'LastPass', 'url': 'https://www.lastpass.com', 'category': categories['工具'], 'description': '密码管理器', 'order': 3},
        {'title': 'Cloudflare', 'url': 'https://www.cloudflare.com', 'category': categories['工具'], 'description': 'CDN和网络安全服务', 'order': 4},
        {'title': 'Vercel', 'url': 'https://vercel.com', 'category': categories['工具'], 'description': '网站部署平台', 'order': 5},
        
        # 社交
        {'title': 'Twitter', 'url': 'https://twitter.com', 'category': categories['社交'], 'description': '社交媒体平台', 'order': 1},
        {'title': 'Instagram', 'url': 'https://www.instagram.com', 'category': categories['社交'], 'description': '图片分享社交平台', 'order': 2},
        {'title': 'Facebook', 'url': 'https://www.facebook.com', 'category': categories['社交'], 'description': '社交网络平台', 'order': 3},
        {'title': 'TikTok', 'url': 'https://www.tiktok.com', 'category': categories['社交'], 'description': '短视频社交平台', 'order': 4},
        {'title': 'Discord', 'url': 'https://discord.com', 'category': categories['社交'], 'description': '游戏社交平台', 'order': 5},
        
        # 健康
        {'title': 'MyFitnessPal', 'url': 'https://www.myfitnesspal.com', 'category': categories['健康'], 'description': '健康饮食追踪', 'order': 1},
        {'title': 'Strava', 'url': 'https://www.strava.com', 'category': categories['健康'], 'description': '运动追踪平台', 'order': 2},
        {'title': 'Headspace', 'url': 'https://www.headspace.com', 'category': categories['健康'], 'description': '冥想应用', 'order': 3},
        {'title': 'Calm', 'url': 'https://www.calm.com', 'category': categories['健康'], 'description': '冥想和睡眠应用', 'order': 4},
        {'title': 'Fitbit', 'url': 'https://www.fitbit.com', 'category': categories['健康'], 'description': '健康追踪设备', 'order': 5},
    ]
    
    # 添加更多网站
    more_sites = [
        # 开发工具
        {'title': 'VS Code', 'url': 'https://code.visualstudio.com', 'category': categories['工具'], 'description': '代码编辑器', 'order': 6},
        {'title': 'Docker', 'url': 'https://www.docker.com', 'category': categories['工具'], 'description': '容器化平台', 'order': 7},
        {'title': 'Postman', 'url': 'https://www.postman.com', 'category': categories['工具'], 'description': 'API测试工具', 'order': 8},
        {'title': 'GitLab', 'url': 'https://gitlab.com', 'category': categories['工具'], 'description': '代码托管平台', 'order': 9},
        {'title': 'Jenkins', 'url': 'https://www.jenkins.io', 'category': categories['工具'], 'description': '持续集成工具', 'order': 10},
        
        # 学习资源
        {'title': 'LeetCode', 'url': 'https://leetcode.com', 'category': categories['学习'], 'description': '编程题库', 'order': 6},
        {'title': 'Codecademy', 'url': 'https://www.codecademy.com', 'category': categories['学习'], 'description': '编程学习平台', 'order': 7},
        {'title': 'freeCodeCamp', 'url': 'https://www.freecodecamp.org', 'category': categories['学习'], 'description': '免费编程学习平台', 'order': 8},
        {'title': 'W3Schools', 'url': 'https://www.w3schools.com', 'category': categories['学习'], 'description': 'Web开发教程', 'order': 9},
        {'title': 'CodePen', 'url': 'https://codepen.io', 'category': categories['学习'], 'description': '前端代码展示平台', 'order': 10},
        
        # 设计资源
        {'title': 'Dribbble', 'url': 'https://dribbble.com', 'category': categories['工作'], 'description': '设计师作品展示', 'order': 6},
        {'title': 'Behance', 'url': 'https://www.behance.net', 'category': categories['工作'], 'description': '创意设计平台', 'order': 7},
        {'title': 'Adobe Creative Cloud', 'url': 'https://www.adobe.com/creativecloud.html', 'category': categories['工作'], 'description': '创意软件套件', 'order': 8},
        {'title': 'Sketch', 'url': 'https://www.sketch.com', 'category': categories['工作'], 'description': '设计工具', 'order': 9},
        {'title': 'InVision', 'url': 'https://www.invisionapp.com', 'category': categories['工作'], 'description': '原型设计工具', 'order': 10},
        
        # 娱乐平台
        {'title': 'Disney+', 'url': 'https://www.disneyplus.com', 'category': categories['娱乐'], 'description': '迪士尼流媒体服务', 'order': 6},
        {'title': 'Amazon Prime', 'url': 'https://www.amazon.com/prime', 'category': categories['娱乐'], 'description': '亚马逊流媒体服务', 'order': 7},
        {'title': 'HBO Max', 'url': 'https://www.hbomax.com', 'category': categories['娱乐'], 'description': 'HBO流媒体服务', 'order': 8},
        {'title': 'Crunchyroll', 'url': 'https://www.crunchyroll.com', 'category': categories['娱乐'], 'description': '动漫流媒体服务', 'order': 9},
        {'title': 'SoundCloud', 'url': 'https://soundcloud.com', 'category': categories['娱乐'], 'description': '音乐分享平台', 'order': 10},
        
        # 社交平台
        {'title': 'Snapchat', 'url': 'https://www.snapchat.com', 'category': categories['社交'], 'description': '即时通讯应用', 'order': 6},
        {'title': 'Pinterest', 'url': 'https://www.pinterest.com', 'category': categories['社交'], 'description': '图片分享平台', 'order': 7},
        {'title': 'Tumblr', 'url': 'https://www.tumblr.com', 'category': categories['社交'], 'description': '博客平台', 'order': 8},
        {'title': 'Reddit', 'url': 'https://www.reddit.com', 'category': categories['社交'], 'description': '社交新闻网站', 'order': 9},
        {'title': 'Quora', 'url': 'https://www.quora.com', 'category': categories['社交'], 'description': '问答平台', 'order': 10},
        
        # 健康应用
        {'title': 'Nike Training Club', 'url': 'https://www.nike.com/training', 'category': categories['健康'], 'description': '运动训练应用', 'order': 6},
        {'title': 'Yoga Studio', 'url': 'https://www.yogastudio.com', 'category': categories['健康'], 'description': '瑜伽应用', 'order': 7},
        {'title': 'Sleep Cycle', 'url': 'https://www.sleepcycle.com', 'category': categories['健康'], 'description': '睡眠追踪应用', 'order': 8},
        {'title': 'MyTherapy', 'url': 'https://www.mytherapyapp.com', 'category': categories['健康'], 'description': '用药提醒应用', 'order': 9},
        {'title': 'WaterMinder', 'url': 'https://waterminder.com', 'category': categories['健康'], 'description': '饮水提醒应用', 'order': 10},
    ]
    
    navigations.extend(more_sites)
    
    # 创建导航链接
    for nav in navigations:
        Navigation.objects.create(**nav)

def remove_preset_navigations(apps, schema_editor):
    Category = apps.get_model('core', 'Category')
    Navigation = apps.get_model('core', 'Navigation')
    Category.objects.all().delete()
    Navigation.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_preset_navigations, remove_preset_navigations),
    ] 