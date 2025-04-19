
struct V1
{
    virtual int a() const = 0;

    int x;
};

struct V2
{
    virtual int b() const = 0;

    int y;
};

struct W1 : V1
{
    virtual int a() const override { return x; }
};

struct W2 : V2
{
    virtual int b() const override { return y; }
};

struct A : public W1, W2
{
    int z;
};

int test1(V1 const* v)
{
    return v->a();
}

int test2(V2 const* v)
{
    return v->b();
}

int testa(A const* a)
{
    return a->b() * a->a() + a->z;
}
