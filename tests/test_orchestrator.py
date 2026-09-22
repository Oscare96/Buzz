from buzz.core.orchestrator import BuzzOrchestrator, BuzzState


def test_orchestrator_starts_idle():
    buzz = BuzzOrchestrator()
    assert buzz.state is BuzzState.IDLE


def test_orchestrator_state_transition():
    buzz = BuzzOrchestrator()
    buzz.set_state(BuzzState.LISTENING)
    assert buzz.state is BuzzState.LISTENING
