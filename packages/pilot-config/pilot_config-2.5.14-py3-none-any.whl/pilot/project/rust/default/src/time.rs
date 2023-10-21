use core::task::Poll;
use futures::future;
use pilot_types::sync::SyncCell;

/// Number of microseconds in a second.
pub const SECOND: u64 = 1_000_000;

/// The system timestamp in microseconds.
static CURRENT_TIME: SyncCell<u64> = SyncCell::new(0);

/// Returns the current system time in microseconds.
pub fn current_time() -> u64 {
    CURRENT_TIME.get()
}

/// Sets the global system time to the given timestamp.
///
/// This method should be only called from `run`.
pub fn set_system_time(us: u64) {
    CURRENT_TIME.set(us)
}

/// Waits until the system time passes the given timestamp in microseconds.
pub async fn wait_until(time: u64) {
    future::poll_fn(|_| {
        if current_time() >= time {
            Poll::Ready(())
        } else {
            Poll::Pending
        }
    })
    .await
}

/// Waits the given number of microseconds.
pub async fn wait_us(duration_us: u64) {
    wait_until(current_time() + duration_us).await
}

/// Waits until the next call to `run`.
pub async fn wait_next_cycle() {
    wait_us(1).await
}
