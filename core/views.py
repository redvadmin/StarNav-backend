from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView as BaseTokenRefreshView
from django.contrib.auth import get_user_model, authenticate
from .models import Category, Navigation, UserNote, UserSettings
from .serializers import (
    UserSerializer, CategorySerializer, NavigationSerializer,
    UserNoteSerializer, UserSettingsSerializer
)

User = get_user_model()

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()

    def get_queryset(self):
        if self.action == 'list' and not self.request.user.is_staff:
            return User.objects.filter(id=self.request.user.id)
        return self.queryset

    @action(detail=False, methods=['get', 'put'])
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = self.get_serializer(request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """修改密码接口"""
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        # 验证数据完整性
        if not all([old_password, new_password, confirm_password]):
            return Response({
                'error': '请提供所有必要的密码字段'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 验证新密码的一致性
        if new_password != confirm_password:
            return Response({
                'error': '两次输入的新密码不一致'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 验证旧密码是否正确
        if not user.check_password(old_password):
            return Response({
                'error': '原密码错误'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 验证新密码是否与旧密码相同
        if old_password == new_password:
            return Response({
                'error': '新密码不能与原密码相同'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 修改密码
        user.set_password(new_password)
        user.save()

        # 生成新的token
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'status': 'success',
            'message': '密码修改成功',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': '请提供用户名和密码'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        else:
            return Response(
                {'error': '用户名或密码错误'},
                status=status.HTTP_401_UNAUTHORIZED
            )

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields = ['is_active']
    search_fields = ['name']
    ordering_fields = ['order', 'name']

class NavigationViewSet(viewsets.ModelViewSet):
    queryset = Navigation.objects.all()
    serializer_class = NavigationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields = ['category', 'is_active']
    search_fields = ['title', 'description']
    ordering_fields = ['order', 'title']
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
        
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def move_up(self, request, pk=None):
        """上移导航项（减小order值）"""
        navigation = self.get_object()
        category_id = navigation.category_id
        current_order = navigation.order
        
        # 查找同一分类中order值小于当前item且最接近的item
        prev_item = Navigation.objects.filter(
            category_id=category_id, 
            order__lt=current_order
        ).order_by('-order').first()
        
        if prev_item:
            # 交换order值
            prev_order = prev_item.order
            prev_item.order = current_order
            navigation.order = prev_order
            
            prev_item.save()
            navigation.save()
            
            return Response({'status': 'success', 'message': '上移成功'})
        else:
            return Response(
                {'status': 'error', 'message': '已经是第一项，无法上移'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def move_down(self, request, pk=None):
        """下移导航项（增加order值）"""
        navigation = self.get_object()
        category_id = navigation.category_id
        current_order = navigation.order
        
        # 查找同一分类中order值大于当前item且最接近的item
        next_item = Navigation.objects.filter(
            category_id=category_id, 
            order__gt=current_order
        ).order_by('order').first()
        
        if next_item:
            # 交换order值
            next_order = next_item.order
            next_item.order = current_order
            navigation.order = next_order
            
            next_item.save()
            navigation.save()
            
            return Response({'status': 'success', 'message': '下移成功'})
        else:
            return Response(
                {'status': 'error', 'message': '已经是最后一项，无法下移'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class UserNoteViewSet(viewsets.ModelViewSet):
    serializer_class = UserNoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserNote.objects.filter(user=self.request.user)

class UserSettingsViewSet(viewsets.ModelViewSet):
    serializer_class = UserSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserSettings.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # 如果已存在设置，则更新而不是创建
        settings, created = UserSettings.objects.get_or_create(
            user=request.user,
            defaults=request.data
        )
        if not created:
            serializer = self.get_serializer(settings, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            serializer = self.get_serializer(settings)
        return Response(serializer.data)

class TokenRefreshView(BaseTokenRefreshView):
    permission_classes = [AllowAny]
