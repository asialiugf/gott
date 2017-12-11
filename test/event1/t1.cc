
#include <iostream>
#include <assert.h>
#include <queue>
#include <string>
//#include <Windows.h>
//#include <process.h>

typedef int s32;
typedef unsigned u32;
typedef float f32;

class LockObject  
{  
public:  
    LockObject()  
    {  
        InitializeCriticalSection(&mLock);  
    }  
    ~LockObject()  
    {  
        DeleteCriticalSection(&mLock);  
    }  

    void Lock()  
    {  
        EnterCriticalSection(&mLock);     
    }  

    void UnLock()  
    {  
        LeaveCriticalSection(&mLock);  
    }  

    bool TryLock()  
    {  
        return TryEnterCriticalSection(&mLock);  
    }  
private:  
    LockObject(const LockObject &other)  
    {}  
    LockObject& operator = (const LockObject &other)  
    {}  
private:  
    CRITICAL_SECTION mLock;  
};  
class ScopeLock  
{  
public:  

    ScopeLock(CRITICAL_SECTION &lock)  
        :mlock(lock)  
    {  
        EnterCriticalSection(&mlock);  
    }  
    ScopeLock(LockObject &lock)  
        :mlock( reinterpret_cast<CRITICAL_SECTION&>(lock) )  
    {  
        EnterCriticalSection(&mlock);  
    }  
    ~ScopeLock()  
    {  
        LeaveCriticalSection(&mlock);  
    }  

private:  
    ScopeLock( const ScopeLock &other)  
        :mlock(other.mlock)  
    {}  
    ScopeLock& operator = (const ScopeLock &other)  
    {}  
private:  
    CRITICAL_SECTION &mlock;  
};

//简单模拟多线程事件驱动,同步通知到主线程
class SimpleEventDriver
{
    public:

        void DrivingEvents( f32 delta )
        {
            ScopeLock Lock( mLockEvents );
            if( mEvents.empty() )
            {
                return;
            }
            const auto &evt = mEvents.front();

            //这里应该调用注册函数，未完待续
            printf( "%s\n", evt.mInfo.c_str() );
            mEvents.pop();
        }

        void OnNotifyEvent( const std::string &info )
        {
            Event evt;
            evt.mInfo = info;
            ScopeLock Lock( mLockEvents );
            mEvents.push( evt );
        }

    private:

        struct Event
        {
            std::string mInfo;
        };

        std::queue< Event > mEvents;

        LockObject mLockEvents;
};

SimpleEventDriver g_EventDriver;

class Test
{
    public:

        void DoSomeThing1()
        {
            g_EventDriver.OnNotifyEvent( "DoSomeThing1 was called." );
        }
        
        void DoSomeThing2()
        {
            g_EventDriver.OnNotifyEvent( "ready to begin thread." );
            _beginthreadex( nullptr, 0, Thread, nullptr, 0, nullptr );
        }

    private:

        static u32 WINAPI Thread( LPVOID p )
        {
            while( true )
            {
                g_EventDriver.OnNotifyEvent( "thread sleep 1000 ms." );
                Sleep( 1000 );
            }
            return 0;
        }
};

s32 main()
{
    Test c;
    c.DoSomeThing1();
    c.DoSomeThing2();
    //主线程循环
    u32 delta = 0;
    u32 last = GetTickCount();
    while( true )
    {
        delta = GetTickCount() - last;
        g_EventDriver.DrivingEvents( delta / 1000.0f );
        Sleep( 8 );
        last = GetTickCount();
    }
    return 0;
}
