from pwn import *

context.log_level = 'debug'

sh = remote('babykok.hackable.software', 1337)


solves = {
  'forall A B : Type, ((((A -> B) -> A) -> A) -> B) -> B': '''
    intros A B.
    auto.
  ''',

  # forall A B, A \/ B -> B \/ A.
  'forall A B : Prop, A \\/ B -> B \\/ A': '''
    intros A B.
    intros H.
    destruct H.
    right.
    exact H.
    auto.
  ''',

  # forall A B C D : Prop, (A -> B) /\ (C -> D) /\ A /\ C -> B /\ D
  'forall A B C D: Prop,(A->B)/\\(C->D)/\\A/\\C -> B/\\D.': '''
    intros A B C D.
    intros H.
    destruct H.
    destruct H0.
    destruct H1.
    split.
    apply H.
    exact H1.
    auto.
  ''',


  'forall (C:Prop) (T:Set) (B: T -> Prop), (exists x : T, C -> B x) -> C -> exists x : T, B x.': '''
    intros C T B.
    intros H.
    destruct H.
    exists x.
    apply H.
    exact H0.
  ''',

  'forall (m n: nat),  m + n = n + m.': '''
    intros m n.
    induction m.
    simpl.
    trivial.
    simpl.
    rewrite IHm.
    trivial.
  ''',

  'forall b1 b2, negb (b1 && b2) = orb (negb b1) (negb b2).': '''
    intros b1 b2.
    destruct b1.
    simpl.
    trivial.
    simpl.
    trivial.
  ''',

  # Require Import Arith.Mult.
  'forall m n, (n + m) * (n + m) =  n * n + 2 * n * m + m * m.': '''
    intros M N.
    rewrite mult_plus_distr_r.
    rewrite mult_plus_distr_l.
    rewrite mult_plus_distr_l.
    rewrite plus_assoc.
    cut (2*N*M=N*M+M*N).
    intros H.
    rewrite H.
    rewrite plus_assoc.
    trivial.
    simpl.
    rewrite plus_0_r.
    rewrite mult_plus_distr_r.
    cut (M * N = N * M).
    intros H1.
    rewrite H1.
    trivial.
    apply mult_comm.
  ''',


  'forall (n:nat) (l:list), n < length l -> exists a: A, nth l n = Some a.': '''
    unfold lt.
    intro n.
    induction n as [| n hn].
    simpl.
    intro l.
    destruct l.
    simpl.
    intro H.
    apply le_Sn_O in H.
    contradiction.
    simpl.
    exists a.
    trivial.
    simpl. 
    destruct l.
    simpl.
    intros H.
    apply le_Sn_O in H.
    contradiction.
    simpl.
    intros H.
    apply le_S_n in H.
    apply hn in H.
    exact H.
  ''',
}

while True:
  question = sh.recvuntil('\n> ')
  print(question)
  for ques in solves:
    ans = solves[ques]

    if ques in question:
      ans = map(lambda x: x.strip(), ans.strip().split('\n'))
      sh.sendline(ans[0])
      for line in ans[1:]:
        sh.sendlineafter('\n> ', line)
      break
  else:
    print(question)
    sh.interactive()

"""
Last Question

Require Import Le.
Section last_stage.
  Variable A : Type.

  Inductive list : Type  :=
   | nil : list
   | cons : A -> list -> list.


  Fixpoint nth (l : list) (n : nat) : option A :=
    match n,l with
      | 0, cons x xs  => Some x
      | S n, cons _ xs  => nth xs n
      | _, _ => None
    end.

  Fixpoint length (l:list) : nat :=
    match l with
      | nil => 0
      | cons _ xs => 1 + length xs
    end.
Theorem nth_in:  forall (n:nat) (l:list), n < length l -> exists a: A, nth l n = Some a.
"""
